import requests
import fileinput
from bs4 import BeautifulSoup as BS


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


def parse_html(file_date, fo):
    """Process html source and returns a dictionary of date and
    results base on a given date.

    Args:
        fo: file open
        file_date: must be in date day month year format
        ex. 10 thu dec 2018
    """
    split_date = file_date.strip().split()
    month = convert_month(split_date[3])
    year = int(split_date[4])
    code = ""
    output = []

    while code != 404:
        content, code = fetch_html(month, year)
        soup = BS(content, "html.parser")
        entries = soup.find_all("div", class_="result")

        prev_date = " ".join(split_date[1:5])
        prev_time = int(split_date[-1])

        for x in entries:
            curr_date = x.h4.time.get_text().split(" ")
            format_date = "{:02} {} {} {}".format(
                int(curr_date[1]),
                curr_date[0][:3].lower(),
                curr_date[2][:3].lower(),
                curr_date[3].lower())

            format_results = [y.get_text()
                              for y in x.select("tbody > tr > td > span")
                              if y.get_text() != "-"]

            date_results = {
                "date": format_date,
                "results": format_results
            }

            # If entries are ordered in descending order
            # output.insert(0, date_results)

            output.append(date_results)

        if month == 12:
            month = 1
            year = year + 1
        else:
            month += 1

    """prev_date and e["date"] must be in format
    01 mon jan 2018"""
    index = [int(i) for i, e in enumerate(output)
             if e["date"] == prev_date][0]

    for item in output[index:]:
        date = item["date"]
        results = item["results"]
        time = len(results) - 1

        if date == prev_date:
            for digits in results[prev_time + 1:]:
                prev_time = time
                fo.write("{}\n".format(digits))
                print(digits)
        else:
            for digits in results:
                prev_date = date
                prev_time = time
                fo.write("{}\n".format(digits))
                print(digits)

    print("Results are up to date for sw3_results_v1.py.")
    return "update: {} {}".format(prev_date, prev_time)


def main():
    file_name = "results_v1.txt"
    with open(file_name, "r+") as f1:
        file_date = f1.readline().strip()
        date_time = parse_html(file_date, f1)

    with fileinput.input(file_name, inplace=True) as f2:
        for line in f2:
            if " " in line:
                print(date_time)
            else:
                print(line, end="")


if __name__ == "__main__":
    main()
