"""
Provided a month_year(str) and a pair(str)
determine count the results that contain
that pair
"""

from re import split


def digits_match(res, combi):
    """Returns True if the given res("123") does contain any pair
    combiantions from combi("342")"""

    for digit in combi:
        if digit in res:
            res = res.replace(digit, "", 1)

    if len(res) == 1 or not res:
        return True
    else:
        return False


def filter_result(month_year, combi):
    all_results = []
    count_results = {}

    with open("results_v2.txt", "r") as fi:
        for line in fi:
            line = line.strip()
            if month_year in line:
                results = split(r"\s{2,}", line)[1:]
                all_results.extend(results)

    for res in all_results:
        if digits_match(res, combi):
            sorted_res = "".join(sorted(res))
            count_results.setdefault(sorted_res, 0)
            count_results[sorted_res] += 1

    print(count_results)


def main():
    month_year = input("Enter month_year(mmm yyyy): ")
    combi = input("Enter count_missing combi: ")

    filter_result(month_year, combi)


if __name__ == "__main__":
    main()
