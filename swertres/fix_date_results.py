from datetime import datetime, timedelta
from itertools import islice
from re import split
from openpyxl import Workbook
from openpyxl.styles import (NamedStyle, Alignment, Font)


def read_results():
    output = []

    with open("results_v2.txt", "r") as fi:
        # updated: 04 sat jan 2020 2
        check_date = fi.readline().strip()[-1]

        for entry in islice(fi, 1, None):
            entry = split(r"\s{2,}", entry.strip())

            output.append(entry)

        if check_date == "2":
            return output
        else:
            return output[:-1]


# def fix_results():
#     all_results = read_results()
#     output = []

#     for i in range(len(all_results) - 1):
#         first_date = datetime.strptime(all_results[i][0], "%d %B %Y")
#         second_date = datetime.strptime(all_results[i + 1][0], "%d %B %Y")
#         diff_date = second_date - first_date
#         diff_month = second_date.month - first_date.month
#         diff_year = second_date.year - first_date.year

#         if diff_month > 0:
#             output.append(all_results[i])
#             output.append("end_month")
#         elif diff_date.days > 0:
#             output.append(all_results[i])
#             for i in range(1, diff_date.days):
#                 time_fill_obj = first_date + timedelta(days=i)
#                 time_fill_str = time_fill_obj.strftime("%d %B %Y")

#                 if time_fill_obj.day == 1 and time_fill_obj.month == 1:
#                     output.append("end_year"),
#                     output.append([time_fill_str, "", "", ""])
#                 else:
#                     output.append([time_fill_str, "", "", ""])
#         else:
#             output.append(all_results[i])

#     output.append(all_results[-1])

#     return output

def fix_results():
    all_results = read_results()
    output = []
    temp_output = []

    for i in range(len(all_results) - 1):
        first_date = datetime.strptime(all_results[i][0], "%d %a %b %Y")
        second_date = datetime.strptime(all_results[i + 1][0], "%d %a %b %Y")
        diff_month = second_date.month - first_date.month

        if diff_month != 0 or diff_month == -11:
            temp_output.append(all_results[i])
            output.append(temp_output)
            temp_output = []
        else:
            temp_output.append(all_results[i])

    return output


def excel_export():
    results = fix_results()

    # Creating Workbook
    wb = Workbook()
    ws = wb.active

    # Formatting
    cell_style = NamedStyle(
        name="cell_style",
        font=Font(bold=True),
        alignment=Alignment(horizontal="center", vertical="center"),
    )

    wb.add_named_style(cell_style)

    # Control group
    month_gap = 1
    year_gap = 1
    time_str = ["11AM", "4PM", "9PM"]

    for count, res in enumerate(results, start=1):
        if (res == "end_month"):
            month_gap += 3
        elif (res == "end_year"):
            year_gap += 35
            month_gap = 1
        else:

            # Date header
            ws.merge_cells(
                start_row=year_gap,
                end_row=year_gap + 1,
                start_column=1,
                end_column=1
            )

            date_cell = ws.cell(row=year_gap, column=1, value="Date")
            date_cell.style = cell_style

            # ['02', 'January', '2013']
            res_date = res[0].split(" ")
            res_day = res_date[0]
            res_month = res_date[1]
            res_year = res_date[2]

            digits = res[1:]

            # Month header
            ws.merge_cells(
                start_row=year_gap,
                end_row=year_gap,
                start_column=month_gap + 1,
                end_column=month_gap + 3
            )

            month_cell = ws.cell(
                row=year_gap,
                column=month_gap + 1,
                value=f"{res_month} {res_year}")
            month_cell.style = cell_style

            # # Time header
            for c_time, time in enumerate(time_str, start=1):
                ws.cell(
                    row=year_gap + 1,
                    column=month_gap + c_time,
                    value=time
                ).style = cell_style

            # Date entry
            ws.cell(
                row=year_gap + count + 1,
                column=1,
                value=res_day
            ).style = cell_style

            # # Result entry
            # for dg_c, dg in enumerate(digits):
            #     ws.cell(
            #         row=count + 2,
            #         column=dg_c + 2,
            #         value=dg
            #     ).style = cell_style

    wb.save("fix_date_results.xlsx")


def main():
    # excel_export()
    for res in fix_results():
        print(len(res), res[-1])


if __name__ == "__main__":
    main()
