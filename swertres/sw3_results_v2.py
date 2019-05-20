import requests
import fileinput
from time import *
from bs4 import BeautifulSoup as BS
from itertools import islice
from datetime import *


def fetch_html(mo, yr):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3163.100 Safari/537.36"
    }

    year_month_url = "https://www.gidapp.com/lottery/philippines/pcso/suertres/month/{}-{}".format(
        yr, mo)

    r = requests.get(year_month_url, headers=headers)

    return (r.content, r.status_code)


def convert_month(data):
    return {
        "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5,
        "jun": 6, "jul": 7, "aug": 8, "sep": 9, "oct": 10,
        "nov": 11, "dec": 12
    }[data]


def get_results(file_month, file_date, file_year):
    """Fetch results from given file_month, file_date and file_year
    and returns a list of (output, index, status_code)
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


def export_results(output, index, file_date, file_time):
    """Given the output(collected date, results, time), index(
    skip one entry ahead), file_date(for comparison on the web_date),
    file_time(for comparison with the current time results). Return
    the new date and time
    """

    with open("results_v2.txt", "a") as fi:
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
                    fi.write(date)

                    new_line_count = 0
                    for digits in results:
                        print(digits)
                        fi.write("{:>10}".format(digits))
                        new_line_count += 1

                    if new_line_count == 3:
                        fi.write("\n")

    return (date, time)


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
