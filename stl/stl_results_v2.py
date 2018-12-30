import requests
import re
import fileinput
from bs4 import BeautifulSoup as BS

def fetch_html(mo, yr):
  headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3163.100 Safari/537.36"
  }

  year_month_url = "https://www.gidapp.com/lottery/philippines/stl/swer3/month/{}-{}".format(yr, mo)

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
        date_list = f1.readline().strip().split()
        full_file_date = " ".join(date_list[1:5])
        month = convert_month(date_list[3])
        year = date_list[4]
        file_time = int(date_list[5])
        output = []
        code = ""
        index = ""

        while code != 404:
            content, code = fetch_html(month, year)
            soup = BS(content, "html.parser")
            entries = soup.find_all("div", class_="result")

            for i, e in enumerate(entries):
                web_date = e.h4.time.get_text().split(" ")
                format_web_date = "{:02} {} {} {}".format(
                    int(web_date[1]),
                    web_date[0][:3].lower(),
                    web_date[2][:3].lower(),
                    web_date[3].lower())

                if format_web_date == full_file_date:
                    index = i

                format_web_results = [y.get_text() 
                    for y in e.select("tbody > tr > td > span") 
                    if y.get_text() != "-"]


                web_date_results = (
                    format_web_date, format_web_results)

                output.append(web_date_results)

            month += 1

    with open("results_v2.txt", "a") as f2:
        for e in output[index:]:
            full_date, digits = e
            trim_date = "{:10}".format(" ".join(
                    full_date.split()[0:3]))
            curr_time = len(digits) - 1

           
            if full_date == full_file_date:

                for e in digits[file_time + 1:]:
                    print(e)
                    f2.write("{:>13}".format(e))
                
                if curr_time == 2:
                    f2.write("\n")

                file_time = curr_time
            else:

                f2.write(trim_date)
                for i, e in enumerate(digits):
                    print(e)
                    f2.write("{:>13}".format(e))

                    if i == 2:
                        f2.write("\n")


                full_file_date = full_date
                file_time = curr_time

        print("Results are up to date")

    updated_date_time = "updated: {} {}".format(
        full_file_date, file_time)

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