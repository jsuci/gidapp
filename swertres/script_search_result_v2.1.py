"""
Provided a month_year(str) and a pair(str)
determine count the results that contain
that pair
"""

from itertools import *
from re import *
from pprint import *
from datetime import *


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
    filter_result("jun 2018", "24")


if __name__ == "__main__":
    main()
