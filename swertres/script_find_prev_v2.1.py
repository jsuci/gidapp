from datetime import *
from itertools import *
from re import *


def gen_pairs():
    pairs = []
    for first_d in range(0, 10):
        for second_d in range(first_d, 10):
            pairs.append("{}{}".format(first_d, second_d))

    return pairs


def gen_month(year, month):
    date_today = date.today()
    date_before = date(year, month, 1)
    date_list = []

    while date_before <= date_today:
        date_list.append(date_before.strftime("%b %Y").lower())

        date_before += timedelta(days=32)
        date_before = date_before.replace(day=1)

    return date_list


def check_pair(res, pair):
    for pair_digit in pair:
        if pair_digit in res:
            res = res.replace(pair_digit, "", 1)

    if len(res) == 1:
        return True
    else:
        return False


def filter_result(month_year, pair):
    all_results = []
    count_results = {}

    with open("results_v2.txt", "r") as fi:
        for line in fi:
            line = line.strip()
            if month_year in line:
                results = split(r"\s{2,}", line)[1:]
                all_results.extend(results)

    for res in all_results:
        if check_pair(res, pair):
            sorted_res = "".join(sorted(res))
            count_results.setdefault(sorted_res, 0)
            count_results[sorted_res] += 1

    print(count_results)


def main():
    for month in gen_month(2018, 12)[:-1]:
        filter_result(month, "07")


if __name__ == "__main__":
    main()
