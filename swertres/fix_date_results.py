from datetime import datetime, timedelta
from itertools import islice
from re import split
from openpyxl import Workbook


def read_results():
    output = []

    with open("results_v2.txt", "r") as fi:
        check_date = fi.readline().strip()[-1]

        for entry in islice(fi, 1, None):
            entry = split(r"\s{2,}", entry.strip())

            output.append(entry)

        if check_date == "2":
            return output
        else:
            return output[:-1]


def fix_results():
    all_results = read_results()
    output = []

    for i in range(len(all_results) - 1):
        first_date = datetime.strptime(all_results[i][0], "%d %a %b %Y")
        second_date = datetime.strptime(all_results[i + 1][0], "%d %a %b %Y")
        diff_date = second_date - first_date
        diff_year = second_date.year - first_date.year

        if diff_date.days == 1:
            output.append(all_results[i])
        else:
            output.append(all_results[i])
            for i in range(1, diff_date.days):
                time_fill_obj = first_date + timedelta(days=i)
                time_fill_str = time_fill_obj.strftime("%d %a %b %Y")

                if time_fill_obj.day == 1 and time_fill_obj.month == 1:
                    output.append([])
                    output.append([time_fill_str.lower(), "", "", ""])
                else:
                    output.append([time_fill_str.lower(), "", "", ""])

    output.append(all_results[-1])

    return output


def excel_export():
    wb = Workbook()
    ws = wb.active

    ws.merge_cells("A1:A2")
    ws["A1"] = "Date"

    wb.save("fix_date_results.xlsx")


def main():
    excel_export()


if __name__ == "__main__":
    main()
