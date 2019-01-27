"""
Given a digit to search and its current location search all
previous result and output the first three previous result that
has at least 3 same current results.
"""

from itertools import *
import re


def get_combinations(number):
    """Given a number generate a list of permutations"""

    combinations = []
    for combi in permutations(number, 3):
        combinations.append("".join(combi))

    return combinations


def compare_accu_res(accu_prev, accu_curr):
    sort_accu_prev = ["".join(sorted(e)) for e in accu_prev]
    sort_accu_curr = ["".join(sorted(e)) for e in accu_curr]
    match_count = 0

    for number in sort_accu_curr:
        if number in sort_accu_prev:
            match_count += 1

    if match_count >= 3:
        return True
    else:
        return False


def get_curr_results(date, number, position):
    """Given a date, number and its position get the prev, curr and
    nxt results relative to the given number and return
    a list of the prev, curr and nxt results
        ex. get_curr_results("22 tue jan 2019", "820", "2")
        >>> [057, 288, 803...]
    """
    with open("results_v2.txt") as fi:
        entries = [re.split(r"\s{10}", e.strip()) for e in fi]
        index = 0

        while index < len(entries) - 1:
            if ((date in entries[index]) and
                    (number in entries[index])):

                prev = entries[index - 1][1:]
                curr = entries[index][1:]
                nxt = entries[index + 1][1:]

                return list(chain(prev, curr, nxt))
            index += 1


def get_prev_results(date, number, position):
    curr_month = date.split(" ")[2].strip()
    curr_year = date.split(" ")[3].strip()
    position = int(position)
    accu_curr_res = get_curr_results(date, number, position)

    for combi in get_combinations(number):

        with open("results_v2.txt") as fi:
            entries = [re.split(r"\s{10}", e.strip()) for e in fi]
            index = 0

            while index < len(entries) - 1:

                if (
                    (curr_month in entries[index][0]) and
                    (combi in entries[index]) and
                    (entries[index].index(combi) == position)
                ):

                    prev = entries[index - 1]
                    curr = entries[index]
                    nxt = entries[index + 1]

                    accu_prev_res = list(chain(
                        prev[1:], curr[1:], nxt[1:]))
                    prev_year = prev[0].split(" ")[3].strip()

                    if (
                        compare_accu_res(accu_prev_res, accu_curr_res) and
                        curr_year != prev_year
                    ):
                        print(prev)
                        print(curr)
                        print(nxt)

                index += 1


def main():
    inputs = ["22 tue jan 2019", "614", "3"]
    get_prev_results(*inputs)


if __name__ == "__main__":
    main()
