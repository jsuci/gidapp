from datetime import datetime, timedelta
from pathlib import Path
from requests_html import HTMLSession, HTML
from fake_useragent import UserAgent
import fileinput


class SW3():
    def __init__(self):
        self.fp = Path("results_v2.txt")

        with open(self.fp, "r") as f:
            line = f.readline()[9:25].strip()
            self.file_date = datetime.strptime(line, "%d %a %b %Y").date()
            self.curr_date = datetime.now().date()

            self.str_file_date = datetime.strftime(
                self.file_date, "%d %a %b %Y").lower()

            self.str_blank_results = (
                f"{'-  ':<12}{'-  ':<12}{'-  '}"
            )

    def get_html(self):
        file_year = self.file_date.year
        file_month = self.file_date.month
        curr_year = self.curr_date.year
        curr_month = self.curr_date.month

        html = ""

        fp = Path(f"html/{file_year}_{file_month}.html")
        cp = Path(f"html/{curr_year}_{curr_month}.html")

        if cp.exists():
            cp.unlink()
            print("remove", cp)

        if fp.exists():
            with open(fp, "r") as f:
                html = HTML(html=f.read())
            print("reading", fp)
        else:
            print("fetching online")
            ua = UserAgent()
            url = (
                f"http://128.199.93.100/lottery/philippines/"
                f"pcso/suertres/month/{file_year}-{file_month}"
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
        output = {}

        for e in entries:

            web_date = datetime.strptime(
                e.xpath("//time/@datetime")[0], "%Y-%m-%d").date()
            web_results = list(
                map(lambda x: x.text, e.xpath("//tr[@class='top']/td")))

            str_web_date = datetime.strftime(
                web_date, "%d %a %b %Y").lower()

            str_web_resu = (
                f"{web_results[0]:<12}"
                f"{web_results[1]:<12}"
                f"{web_results[2]}"
            )

            output[str_web_date] = str_web_resu

        return output

    def add_day(self):
        self.file_date += timedelta(days=1)
        self.str_file_date = datetime.strftime(
            self.file_date, "%d %a %b %Y").lower()

    def get_results(self):

        temp_month = self.file_date.month
        temp_html = self.get_html()

        while self.file_date != self.curr_date:
            self.add_day()
            blank_output = (
                f"{self.str_file_date:<21}"
                f"{self.str_blank_results}"
            )

            with open(self.fp, "a") as fo:

                if temp_month != self.file_date.month:
                    temp_month = self.file_date.month
                    temp_html = self.get_html()

                if self.str_file_date in temp_html:
                    date_res = (
                        f"{self.str_file_date:<21}"
                        f"{temp_html[self.str_file_date]}"
                    )
                    fo.write(f"{date_res}\n")
                else:
                    fo.write(f"{blank_output}\n")

        with fileinput.input(self.fp, inplace=True) as fio:
            for entry in fio:
                if ":" in entry:
                    print(f"updated: {self.str_file_date}")
                else:
                    date_entry = entry[:15]

                    if date_entry in temp_html:
                        found_date_res = (
                            f"{date_entry:<21}"
                            f"{temp_html[date_entry]}"
                        )
                        print(found_date_res)
                    else:
                        print(entry, end="")


def main():
    sw3 = SW3()
    sw3.get_results()


if __name__ == "__main__":
    main()
