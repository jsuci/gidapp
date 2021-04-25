from openpyxl import Workbook
from openpyxl.styles import (
    NamedStyle, Alignment, Font,
    PatternFill, Border, Side
)
from itertools import islice


def get_results():
    results = []

    with open("results_v2.txt", "r") as fi:
        for line in islice(fi, 2, None):
            l_list = line.strip().split()
            day = l_list[1]
            nums = l_list[4:]
            results.append((day, nums))

    return results


def class_results():
    results = get_results()
    class_res = [
        ("sun", []),
        ("mon", []),
        ("tue", []),
        ("wed", []),
        ("thu", []),
        ("fri", []),
        ("sat", [])
    ]

    for res in results:
        if res[0] == "sun":
            class_res[0][1].extend(res[1])

        if res[0] == "mon":
            class_res[1][1].extend(res[1])

        if res[0] == "tue":
            class_res[2][1].extend(res[1])

        if res[0] == "wed":
            class_res[3][1].extend(res[1])

        if res[0] == "thu":
            class_res[4][1].extend(res[1])

        if res[0] == "fri":
            class_res[5][1].extend(res[1])

        if res[0] == "sat":
            class_res[6][1].extend(res[1])

    return class_res


def write_to_excel(user_num, wb, cell_style):

    wb.create_sheet(user_num)
    ws = wb[user_num]

    class_res = class_results()

    # cres = ("sun, ["123", "456"]")
    for col, cres in enumerate(class_res):
        col_loc = col + 1

        day_cell = ws.cell(column=col_loc, row=1, value=cres[0])
        day_cell.style = cell_style

        for row, num in enumerate(cres[1]):
            row_loc = row + 2

            num_cell = ws.cell(column=col_loc, row=row_loc, value=f"{num}")
            num_cell.style = cell_style

            if check_num(user_num, num):
                num_cell.fill = PatternFill("solid", fgColor="ffffff")


def check_num(user_num, my_num):
    fdigits = []

    for num in user_num:
        if num in my_num:
            fdigits.append(num)
            my_num = my_num.replace(num, '', 1)

    if len(fdigits) >= 1:
        return True
    else:
        return False


def main():
    wb = Workbook()

    bd = Side(style="thin", color="555555")
    cell_style = NamedStyle(
        name="cell_style",
        font=Font(size=15, bold=False),
        alignment=Alignment(horizontal="center", vertical="center"),
        border=Border(top=bd, bottom=bd, right=bd, left=bd),
        fill=PatternFill("solid", fgColor="6699ff")
    )

    wb.add_named_style(cell_style)

    dest_name = "excel_results_2.xlsx"

    for i in range(10):
        user_num = str(i)
        write_to_excel(user_num, wb, cell_style)

    del wb["Sheet"]
    wb.save(filename=dest_name)

    print("Done exporting excel_results_2.xlsx")


if __name__ == "__main__":
    main()
