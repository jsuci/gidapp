import requests
import fileinput
from datetime import datetime
from time import sleep
from bs4 import BeautifulSoup as BS
from itertools import islice
from random import choice


def rand_ua():
    """
    INPUT:
        user_agents.txt - a text file containing all user-agent strings
        from chrome and firefox

    OUTPUT
        output - a random user-agent string
    """

    non_rand = []

    with open("../user_agents.txt") as file:
        for line in file:
            non_rand.append(line.strip())

    output = choice(non_rand)

    return output


def fetch_html(mo, yr):
    headers = {
        "user-agent": rand_ua(),
        "referer": "https://www.google.com/",
        "upgrade-insecure-requests": "1"
    }

    year_month_url = (
        f"https://www.gidapp.com/lottery/philippines/"
        f"stl/swer3/month/{yr}-{mo}"
    )

    r = requests.get(year_month_url, headers=headers)

    return (r.content, r.status_code)


def convert_month(data):
    return {
        "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5,
        "jun": 6, "jul": 7, "aug": 8, "sep": 9, "oct": 10,
        "nov": 11, "dec": 12
    }[data]


def export_results(output, index, file_date, file_time):
    """Given the output(collected date, results, time), index(
    skip one entry ahead), file_date(for comparison on the web_date),
    file_time(for comparison with the current time results). Return
    the new date and time
    """

    with open("results_v1.txt", "a") as fi:
        for date_results_time in islice(output, index, None):
            date, results, time = date_results_time

            """Check if entries in file are identical to the ones
            on the web. If they are then skip and process the next
            entry.
            """
            if date == file_date and time == file_time:
                continue
            else:
                if date == file_date:
                    digit_index = file_time + 1

                    for digits in islice(results, digit_index, None):
                        fi.write("{}\n".format(digits))
                        print(digits)
                else:
                    for digits in results:
                        fi.write("{}\n".format(digits))
                        print(digits)

    return (date, time)


def update_file_date_time(new_date, new_time):
    updated_date_time = "updated: {} {}".format(
        new_date, new_time)

    with fileinput.input("results_v1.txt", inplace=True) as fio:
        for entry in fio:
            if ":" in entry:
                print(updated_date_time)
            else:
                print(entry, end="")


def get_results(file_month, file_date, file_year):
    """Give a converted month, date and year, fetch and filter gidapp
    website and return a list of tuple output, index, status_code
    """

    # A list of tuples: [(date, [results],...)]
    output = []
    status_code = ""
    index = 0
    end_date = ""

    content, status_code = fetch_html(file_month, file_year)
    soup = BS(content, "html.parser")
    entries = soup.find_all("div", class_="result")

    for i, e in enumerate(entries):
        # Sunday, February 10, 2019 format
        web_date_list = datetime.strptime(
            e.h5.time.get("datetime"), "%Y-%m-%d")

        # date, day, month, year
        web_date = web_date_list.strftime("%d %a %b %Y").lower()

        web_results = [y.get_text() for y in e.select(
            "tbody > tr > td > span") if y.get_text() != "-"]
        web_date_results_time = (web_date, web_results, len(
            web_results) - 1)

        if web_date == file_date:
            index = i

        output.append(web_date_results_time)

        end_date = output[-1][0]

    return (output, end_date, index, status_code)


def main():
    with open("results_v1.txt", "r") as fi:
        file_date_list = fi.readline().strip().split()
        file_date = " ".join(file_date_list[1:5])
        file_month = convert_month(file_date_list[3])
        file_year = int(file_date_list[4])
        file_time = int(file_date_list[5])

    while True:
        curr_date = file_date
        output, curr_date, index, status_code = get_results(
            file_month, curr_date, file_year)

        if status_code != 404:
            new_date, new_time = export_results(
                output, index, file_date, file_time)

            update_file_date_time(new_date, new_time)

            if file_month == 12:
                file_month = 1
                file_year = file_year + 1
            else:
                file_month += 1

            sleep(5)
        else:
            break

    print("Results are now up to date.")


if __name__ == "__main__":
    main()
