from re import split
from sys import argv

from openpyxl import Workbook
from openpyxl.chart import (
    LineChart,
    Reference
)


def get_weekly_results(num_res):

    if not num_res:
        num_res = 120
    else:
        num_res = int(num_res)

    output = {}
    week_count = 1

    with open("results_v2.txt", "r") as fi:

        for entry in list(fi)[-num_res:]:
            entry = split(r"\s{1,}", entry.strip())

            output.setdefault(week_count, [])
            output[week_count].append(entry)

            if entry[1] == 'sat':
                week_count += 1

    return output


def get_num_stats(w_res):
    output = []

    t_digits = 0

    t_even = 0
    t_odd = 0

    t_high = 0
    t_low = 0

    t_high_even = 0
    t_high_odd = 0

    t_low_even = 0
    t_low_odd = 0

    t_pos_1_even = 0
    t_pos_1_odd = 0

    t_pos_2_even = 0
    t_pos_2_odd = 0

    t_pos_3_even = 0
    t_pos_3_odd = 0

    t_pos_1_high = 0
    t_pos_1_low = 0

    t_pos_2_high = 0
    t_pos_2_low = 0

    t_pos_3_high = 0
    t_pos_3_low = 0

    date_range = f"{' '.join(w_res[0][0:3])} - {' '.join(w_res[-1][0:3])}"

    for e_w_res in w_res:
        for e_res in e_w_res[4:]:

            for pos, d in enumerate(e_res, 1):
                if d == '-':
                    continue
                else:
                    d = int(d)

                if pos == 1:
                    if d % 2 == 0:
                        t_pos_1_even += 1
                    else:
                        t_pos_1_odd += 1

                    if d in [1, 2, 3, 4, 5]:
                        t_pos_1_low += 1
                    else:
                        t_pos_1_high += 1
                elif pos == 2:
                    if d % 2 == 0:
                        t_pos_2_even += 1
                    else:
                        t_pos_2_odd += 1

                    if d in [1, 2, 3, 4, 5]:
                        t_pos_2_low += 1
                    else:
                        t_pos_2_high += 1

                else:
                    if d % 2 == 0:
                        t_pos_3_even += 1
                    else:
                        t_pos_3_odd += 1

                    if d in [1, 2, 3, 4, 5]:
                        t_pos_3_low += 1
                    else:
                        t_pos_3_high += 1

                if d in [1, 2, 3, 4, 5]:
                    t_low += 1

                    if d % 2 == 0:
                        t_even += 1
                        t_low_even += 1

                    else:
                        t_odd += 1
                        t_low_odd += 1

                else:
                    t_high += 1

                    if d % 2 == 0:
                        t_even += 1
                        t_high_even += 1

                    else:
                        t_odd += 1
                        t_high_odd += 1

                t_digits += 1

    output.extend([
        date_range,
        t_even,
        t_odd,
        t_high,
        t_low,
        t_high_even,
        t_high_odd,
        t_low_even,
        t_low_odd,
        t_pos_1_even,
        t_pos_1_odd,
        t_pos_2_even,
        t_pos_2_odd,
        t_pos_3_even,
        t_pos_3_odd,
        t_pos_1_high,
        t_pos_1_low,
        t_pos_2_high,
        t_pos_2_low,
        t_pos_3_high,
        t_pos_3_low
    ])

    return output


def plot_rows(rows):

    wb = Workbook()
    ws = wb.active

    for row in rows:
        ws.append(row)

    t_col_count = len(rows[0])
    t_row_count = len(rows) - 1  # adjust row entries here
    chart_gap = 15

    # even - odd
    c1 = LineChart()
    c1.title = "Even / Odd"
    c1.y_axis.title = 'Probability'
    c1.x_axis.title = 'Week Count'
    c1.width = 27

    data = Reference(ws, min_col=3, min_row=1, max_col=4, max_row=t_row_count)
    c1.add_data(data, titles_from_data=True)

    ws.add_chart(c1, f'A{t_row_count + 3}')

    # high - low
    c2 = LineChart()
    c2.title = "High / Low"
    c2.y_axis.title = 'Probability'
    c2.x_axis.title = 'Week Count'
    c2.width = 27

    data = Reference(ws, min_col=5, min_row=1, max_col=6, max_row=t_row_count)
    c2.add_data(data, titles_from_data=True)

    ws.add_chart(c2, f'A{t_row_count + chart_gap + 3}')

    # high even / odd
    c3 = LineChart()
    c3.title = "High Even / Odd"
    c3.y_axis.title = 'Probability'
    c3.x_axis.title = 'Week Count'
    c3.width = 27

    data = Reference(ws, min_col=7, min_row=1, max_col=8, max_row=t_row_count)
    c3.add_data(data, titles_from_data=True)

    ws.add_chart(c3, f'A{t_row_count + chart_gap * 2 + 3}')

    # low even / odd
    c4 = LineChart()
    c4.title = "Low Even / Odd"
    c4.y_axis.title = 'Probability'
    c4.x_axis.title = 'Week Count'
    c4.width = 27

    data = Reference(ws, min_col=9, min_row=1, max_col=10, max_row=t_row_count)
    c4.add_data(data, titles_from_data=True)

    ws.add_chart(c4, f'A{t_row_count + chart_gap * 3 + 3}')

    # pos 1 even / odd
    c5 = LineChart()
    c5.title = "Position 1 Even / Odd"
    c5.y_axis.title = 'Probability'
    c5.x_axis.title = 'Week Count'
    c5.width = 27

    data = Reference(ws, min_col=11, min_row=1,
                     max_col=12, max_row=t_row_count)
    c5.add_data(data, titles_from_data=True)

    ws.add_chart(c5, f'A{t_row_count + chart_gap * 4 + 3}')

    # pos 2 even / odd
    c6 = LineChart()
    c6.title = "Position 2 Even / Odd"
    c6.y_axis.title = 'Probability'
    c6.x_axis.title = 'Week Count'
    c6.width = 27

    data = Reference(ws, min_col=13, min_row=1,
                     max_col=14, max_row=t_row_count)
    c6.add_data(data, titles_from_data=True)

    ws.add_chart(c6, f'A{t_row_count + chart_gap * 5 + 3}')

    # pos 3 even / odd
    c7 = LineChart()
    c7.title = "Position 3 Even / Odd"
    c7.y_axis.title = 'Probability'
    c7.x_axis.title = 'Week Count'
    c7.width = 27

    data = Reference(ws, min_col=15, min_row=1,
                     max_col=16, max_row=t_row_count)
    c7.add_data(data, titles_from_data=True)

    ws.add_chart(c7, f'A{t_row_count + chart_gap * 6 + 3}')

    # pos 1 high / low
    c8 = LineChart()
    c8.title = "Position 1 High / Low"
    c8.y_axis.title = 'Probability'
    c8.x_axis.title = 'Week Count'
    c8.width = 27

    data = Reference(ws, min_col=17, min_row=1,
                     max_col=18, max_row=t_row_count)
    c8.add_data(data, titles_from_data=True)

    ws.add_chart(c8, f'A{t_row_count + chart_gap * 7 + 3}')

    # pos 2 high / low
    c9 = LineChart()
    c9.title = "Position 2 High / Low"
    c9.y_axis.title = 'Probability'
    c9.x_axis.title = 'Week Count'
    c9.width = 27

    data = Reference(ws, min_col=19, min_row=1,
                     max_col=20, max_row=t_row_count)
    c9.add_data(data, titles_from_data=True)

    ws.add_chart(c9, f'A{t_row_count + chart_gap * 8 + 3}')

    # pos 3 high / low
    c9 = LineChart()
    c9.title = "Position 3 High / Low"
    c9.y_axis.title = 'Probability'
    c9.x_axis.title = 'Week Count'
    c9.width = 27

    data = Reference(ws, min_col=21, min_row=1,
                     max_col=22, max_row=t_row_count)
    c9.add_data(data, titles_from_data=True)

    ws.add_chart(c9, f'A{t_row_count + chart_gap * 9 + 3}')

    wb.save("excel_results_5.xlsx")


def main():

    # enter number of results to process
    week_res = get_weekly_results(argv[1:])
    rows = [
        [
            'WEEK_COUNT', 'DATE_RANGE', 'EVEN', 'ODD', 'HIGH', 'LOW',
            'HIGH_EVEN', 'HIGH_ODD', 'LOW_EVEN', 'LOW_ODD',
            'POS_1_EVEN', 'POS_1_ODD', 'POS_2_EVEN',
            'POS_2_ODD', 'POS_3_EVEN', 'POS_3_ODD',
            'POS_1_HIGH', 'POS_1_LOW', 'POS_2_HIGH', 'POS_2_LOW',
            'POS_3_HIGH', 'POS_3_LOW'
        ]
    ]

    for k, v in week_res.items():
        each_row = []

        # add week_count
        each_row.append(k)

        # add date-range to pos_3_odd
        num_stats = get_num_stats(v)
        each_row.extend(num_stats)

        rows.append(each_row)

    plot_rows(rows)


if __name__ == "__main__":
    main()
