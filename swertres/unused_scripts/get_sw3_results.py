from datetime import datetime, timedelta
from pathlib import Path
from requests_html import HTMLSession, HTML
from fake_useragent import UserAgent
import fileinput


class SW3():
    def __init__(self):
        fp = Path("results_v2.txt")
        with open(fp, "r") as f:
            line = f.readline()[9:25].strip()
            self.file_date = datetime.strptime(line, "%d %a %b %Y").date()
            self.curr_date = datetime.now().date()

    def compare_date(self):
        if self.file_date == self.curr_date:
            return True
        else:
            return False

    def add_day(self):
        self.file_date += timedelta(days=1)

    def parse_html(self, mode="offline"):
        year = self.file_date.year
        month = self.file_date.month
        html = ""

        fp = Path(f"html/{year}_{month}.html")

        if fp.exists() and mode == "offline":
            with open(fp, "r") as f:
                html = HTML(html=f.read())
        else:
            ua = UserAgent()
            url = (
                f"http://128.199.93.100/lottery/philippines/"
                f"pcso/suertres/month/{year}-{month}"
            )
            headers = {
                "Host": "www.gidapp.com",
                "User-Agent": ua.random
            }

            sess = HTMLSession()
            r = sess.get(url, headers=headers)

            with open(fp, "w") as fo:
                fo.write(r.text)

            html = HTML(html=r.text)

        # returns 0 for non existent html
        entries = html.xpath("//div[contains(@id, 'suertres')]")
        output = []

        for e in entries:

            web_date = datetime.strptime(
                e.xpath("//time/@datetime")[0], "%Y-%m-%d").date()
            web_results = list(
                map(lambda x: x.text, e.xpath("//tr[@class='top']/td")))

            str_web_date = datetime.strftime(
                web_date, "%d %a %b %Y").lower()

            output.append((str_web_date, web_results))

        return output

    def write_to_file(self, entry):
        fp = Path("results_v2.txt")
        output = ""

        if len(entry) == 0:
            str_file_date = datetime.strftime(
                self.file_date, "%d %a %b %Y").lower()
            str_file_results = f"{' ':<9}{'-  ':<12}{'-  ':<12}{'-  '}"

            print(f"{str_file_date:<9}{str_file_results}")
            output = f"{str_file_date:<9}{str_file_results}"
        else:
            str_file_date = datetime.strftime(
                entry[0][0], "%d %a %b %Y").lower()
            str_file_results = (
                f"{' ':<9}{entry[0][1][0]:<12}{entry[0][1][1]:<12}"
                f"{entry[0][1][2]}"
            )

            print(f"{str_file_date:<9}{str_file_results}")
            output = f"{str_file_date:<9}{str_file_results}"

        with open(fp, "a") as fo:
            fo.write(f"{output}\n")

        update_date = f"updated: {str_file_date}"

        with fileinput.input("results_v2.txt", inplace=True) as fio:
            for entry in fio:
                if ":" in entry:
                    print(update_date)
                else:
                    print(entry, end="")

    def get_new_results(self):
        web_res = self.parse_html("online")[-1]
        web_res_date = web_res[0]
        web_res_result = web_res[1]

        # print(web_res_date, web_res_result)
        str_web_date = datetime.strftime(
            web_res_date, "%d %a %b %Y").lower()

        str_file_date = datetime.strftime(
            self.file_date, "%d %a %b %Y").lower()

        str_web_results = (
            f"{' ':<9}{web_res_result[0]:<12}{web_res_result[1]:<12}"
            f"{web_res_result[2]}"
        )

        update_date = f"updated: {str_file_date}"

        output = f"{str_web_date:<9}{str_web_results}"

        # if self.file_date == web_res_date:
        with fileinput.input("results_v2.txt", inplace=True) as fio:
            for entry in fio:
                if ":" in entry:
                    print(update_date)
                elif str_web_date in entry:
                    print(output)
                else:
                    print(entry, end="")

        print("results up to date.")


def main():
    sw3 = SW3()

    while not sw3.compare_date():

        sw3.add_day()

        results = sw3.parse_html()
        entry = [x for x in results if sw3.file_date in x]

        sw3.write_to_file(entry)

    sw3.get_new_results()


if __name__ == "__main__":
    main()
