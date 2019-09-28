import fileinput
from requests import get
from time import sleep
from bs4 import BeautifulSoup as BS
from itertools import islice
from datetime import datetime
from random import choice
from secrets import token_urlsafe


def rand_ua():
    """
    INPUT:
        user_agents.txt - a text file containing all user-agent strings
        from chrome and firefox

    OUTPUT
        output - a random user-agent string (ex. Mozilla/5.0 (X11;
        Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)
        HeadlessChrome/75.0.3770.100 Safari/537.36))
    """

    non_rand = []

    with open("../user_agents.txt") as file:
        for line in file:
            non_rand.append(line.strip())

    output = choice(non_rand)

    return output


def fetch_html(month, year, date):
    """
    INPUT:
        month - a 3 character string representation of month (ex. "jul", "mar")
        year - a string year (ex. "2019", "2017")
        date - an int date (ex. "12")

    OUTPUT:
        (r.text, r.status_code) - a tuple of html source (ex. "<html>...")
        and status code (ex. 200)
    """

    headers = {
        "accept": "text/html",
        "accept-language": "en-US,en;q=0.9",
        "user-agent": rand_ua(),
        "referer": "https://www.google.com"
    }

    year_month_url = (
        f"https://www.gidapp.com/lottery/philippines/"
        f"stl/swer3/month/{year}-{month}/{token_urlsafe(5)}"
    )

    r = get(year_month_url, headers=headers)

    return (r.text, r.status_code)


def get_results(file_month, file_date, file_year):
    """Fetch results from given file_month, file_date and file_year
    and returns a list of(output, index, status_code)
    """

    # A list of tuples: [(date, [results],...)]
    output = []
    status_code = ""
    index = 0
    end_date = ""

    content, status_code = fetch_html(file_month, file_year, file_date)
    soup = BS(content, "html.parser")

    # Result container class="col-md-6 result
    entries = soup.find_all("div", class_="col-md-6 result")

    for i, e in enumerate(entries):
        # <time datetime="2019-07-03">
        web_date = datetime.strptime(
            e.h5.time.get("datetime"), "%Y-%m-%d")

        web_results = [y.get_text() for y in e.select(
            "tbody > tr > td > span") if y.get_text() != "-"]

        # A tuple of (datetime object, list, int)
        web_date_results_time = (web_date, web_results, len(
            web_results) - 1)

        if web_date == file_date:
            index = i

        output.append(web_date_results_time)

        end_date = output[-1][0]

    return (output, end_date, index, status_code)


def export_results(output, index, file_date, file_time):
    """Given the output(collected date, results, time), index(
    skip one entry ahead), file_date(for comparison on the web_date),
    file_time(for comparison with the current time results). Return
    the new date and time
    """

    with open("results_v2.txt", "a") as fi:
        for date_results_time in islice(output, index, None):
            web_date, results, time = date_results_time

            """Check if entries in file are identical to the ones
            on the web. If they are then skip and process the next
            entry.
            """

            strf_web_date = web_date.strftime("%d %a %b %Y").lower()

            if web_date == file_date and time == file_time:
                continue
            else:
                if web_date == file_date:
                    new_line_count = 0
                    digit_index = file_time + 1

                    for digits in islice(results, digit_index, None):
                        print(digits)
                        fi.write("{:>10}".format(digits))
                        new_line_count += 1

                    # Decide when add new line inside file
                    if new_line_count == 2 or digit_index == 2:
                        fi.write("\n")

                else:
                    fi.write(strf_web_date)

                    new_line_count = 0
                    for digits in results:
                        print(digits)
                        fi.write("{:>10}".format(digits))
                        new_line_count += 1

                    if new_line_count == 3:
                        fi.write("\n")

    return (strf_web_date, time)


def update_file_date_time(new_date, new_time):
    updated_date_time = "updated: {} {}".format(
        new_date, new_time)

    with fileinput.input("results_v2.txt", inplace=True) as fio:
        for entry in fio:
            if ":" in entry:
                print(updated_date_time)
            else:
                print(entry, end="")


def main():
    with open("results_v2.txt", "r") as fi:
        file_date_list = fi.readline().strip().split()
        file_date = datetime.strptime(
            " ".join(file_date_list[1:5]), "%d %a %b %Y")
        file_month = file_date.month
        file_year = file_date.year
        file_time = int(file_date_list[5])

    while True:
        curr_date = file_date

        output, curr_date, index, status_code = get_results(
            file_month, curr_date, file_year)

        if status_code == 200:

            new_date, new_time = export_results(
                output, index, file_date, file_time)

            update_file_date_time(new_date, new_time)

            if file_month == 12:
                file_month = 1
                file_year = file_year + 1
            else:
                file_month += 1

            sleep(5)

        # No draws in the month of august
        elif status_code == 500:
            file_month += 1

        else:
            break

    print("Results are now up to date.")


if __name__ == "__main__":
    main()
