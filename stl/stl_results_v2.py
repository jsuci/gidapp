import requests
import fileinput
from bs4 import BeautifulSoup as BS
from itertools import islice


def fetch_html(mo, yr):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3163.100 Safari/537.36"
    }

    year_month_url = "https://www.gidapp.com/lottery/philippines/stl/swer3/month/{}-{}".format(
        yr, mo)

    r = requests.get(year_month_url, headers=headers)

    return (r.content, r.status_code)


def convert_month(data):
    return {
        "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5,
        "jun": 6, "jul": 7, "aug": 8, "sep": 9, "oct": 10,
        "nov": 11, "dec": 12
    }[data]


def parse_html():
    """Process html source and returns all the date and
    results base on the given date from file
    """

    with open("results_v2.txt", "r") as f1:
        file_date_list = f1.readline().strip().split()
        file_date = " ".join(file_date_list[1:5])
        file_month = convert_month(file_date_list[3])
        file_year = int(file_date_list[4])
        file_time = int(file_date_list[5])

        # A list of tuples: (date, [results])
        output = []
        code = ""
        index = ""

        while code != 404:
            content, code = fetch_html(file_month, file_year)
            soup = BS(content, "html.parser")
            entries = soup.find_all("div", class_="result")

            for i, e in enumerate(entries):
                web_date_list = e.h4.time.get_text().split(" ")
                web_date = "{:02} {} {} {}".format(
                    int(web_date_list[1]),
                    web_date_list[0][:3].lower(),
                    web_date_list[2][:3].lower(),
                    web_date_list[3].lower())

                if web_date == file_date:
                    index = i

                web_results = [y.get_text()
                               for y in e.select("tbody > tr > td > span")
                               if y.get_text() != "-"]

                web_date_results = (
                    web_date, web_results)

                output.append(web_date_results)

            if file_month == 12:
                file_month = 1
                file_year = file_year + 1
            else:
                file_month += 1

    with open("results_v2.txt", "a") as f2:
        for e in islice(output, index, None):
            web_date, digits = e
            trim_date = "{:10}".format(" ".join(
                web_date.split()[0:3]))
            web_time = len(digits) - 1
            digit_index = file_time + 1

            if web_date == file_date and file_time == web_time:
                continue
            else:
                if web_date == file_date:
                    new_line_count = 0
                    for e in islice(digits, digit_index, None):
                        print(e)
                        f2.write("{:>13}".format(e))
                        new_line_count += 1

                    if new_line_count == 2 or digit_index == 2:
                        f2.write("\n")

                    file_time = web_time
                else:
                    new_line_count = 0

                    f2.write(trim_date)
                    for e in digits:
                        print(e)
                        f2.write("{:>13}".format(e))
                        new_line_count += 1

                    if new_line_count == 3:
                        f2.write("\n")

                    file_date = web_date
                    file_time = web_time

        print("Results are up to date for sw3_results_v2.py.")

    updated_date_time = "updated: {} {}".format(
        file_date, file_time)

    with fileinput.input("results_v2.txt", inplace=True) as f3:
        for e in f3:
            if ":" in e:
                print(updated_date_time)
            else:
                print(e, end="")


def main():
    parse_html()


if __name__ == "__main__":
    main()
