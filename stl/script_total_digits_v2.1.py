"""
Using the results from results_v2.txt, count the total
digits that appeared on that day
"""

from itertools import *
from re import *


def get_results():
    with open("results_v2.txt", "r") as fi:
        for line in islice(fi, 2, None):
            entries = split(r"\s{2,}", line.strip())
            date = entries[0]
            results = entries[1:]
            uniq_digit, uniq_digit_len = count_digits(results)

            print("{:<20}{:<6}{}".format(date, uniq_digit_len, uniq_digit))


def count_digits(results):
    unique_digits = []

    for digit in chain(*results):
        if digit not in unique_digits:
            unique_digits.append(digit)

    return (unique_digits, len(unique_digits))


def main():
    get_results()


if __name__ == "__main__":
    main()
