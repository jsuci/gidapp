"""
Given a recent date, number and its location search all
previous result that has same month, same location but different
combination of the given and once there is a match get the prev
and nxt results and mark the match digits relative to the current
number
"""

from itertools import *
import re


def mark_compile_res(prev_compile_res, number):
    # Given sorted number and the prev_compile_res mark the
    # prev_compile_res

    result = ()

    for entry in prev_compile_res:
        result += (["{}*".format(e) if sorted(number) == sorted(e)
                    else e for e in entry],)

    return result


def compare_accu_res(curr_res, prev_res):
    # Mark the digit in prev_compile_res where it has a match

    curr_compile_res, curr_chain_res = curr_res
    prev_compile_res, prev_chain_res = prev_res

    sort_accu_prev = ["".join(sorted(e)) for e in prev_chain_res]
    sort_accu_curr = ["".join(sorted(e)) for e in curr_chain_res]
    match_count = 0

    for number in sort_accu_curr:
        if number in sort_accu_prev:
            prev_compile_res = mark_compile_res(prev_compile_res, number)
            match_count += 1

    if match_count >= 3:
        return prev_compile_res
    else:
        return False


def get_combinations(number):
    """Given a number generate a list of permutations"""

    combinations = []
    for combi in permutations(number, 3):
        combinations.append("".join(combi))

    return combinations


def get_curr_results(date, number, position):
    """Given a date, number and its position get the prev, curr and
    nxt results relative to the given number and return
    a tuple of prev, curr, nxt and chained results
        ex. get_curr_results("22 tue jan 2019", "820", "2")
        >>> ((['12 sat jan 2013', '052', '632', '820']..),
        [057, 288, 803...]...)
    """
    with open("results_v2.txt") as fi:
        entries = [re.split(r"\s{2,}", e.strip()) for e in fi]
        index = 0

        while index < len(entries) - 1:
            if ((date in entries[index]) and
                    (number in entries[index])):

                prev = entries[index - 1]
                curr = entries[index]
                nxt = entries[index + 1]

                compiled_curr_res = (prev, curr, nxt)
                accu_curr_res = list(chain(
                    prev[1:], curr[1:], nxt[1:]))

                return (compiled_curr_res, accu_curr_res)

            index += 1


def get_prev_results(date, number, position):
    """Given a date, number and its position get the prev, curr and
    nxt results relative to the given number and return
    a list of tuple containing prev, curr, nxt and chained results
        ex. get_curr_results("22 tue jan 2019", "820", "2")
        >>> [((['12 sat jan 2013', '052', '632', '820']..),
        [057, 288, 803...]...),...]
    """

    combinations = get_combinations(number)
    curr_month = date.split(" ")[2].strip()
    curr_year = date.split(" ")[3].strip()
    curr_position = int(position)

    all_prev_res = []

    for curr_num in combinations:
        with open("results_v2.txt") as fi:
            entries = [re.split(r"\s{2,}", e.strip())
                       for e in islice(fi, 2, None)]
            index = 0

            while index < len(entries) - 1:
                entry_num = entries[index]

                if (curr_num in entry_num):
                    entry_month = entries[index][0].split(" ")[2]
                    entry_year = entries[index][0].split(" ")[3]
                    entry_position = entries[index].index(curr_num)

                    if (
                        (curr_month == entry_month) and
                        (curr_year != entry_year) and
                        (curr_position == entry_position)
                    ):

                        prev = entries[index - 1]
                        curr = entries[index]
                        nxt = entries[index + 1]

                        compiled_prev_res = (prev, curr, nxt)
                        accu_prev_res = list(chain(
                            prev[1:], curr[1:], nxt[1:]))

                        result = (compiled_prev_res, accu_prev_res)

                        if result not in all_prev_res:
                            all_prev_res.append(result)

                index += 1

    return all_prev_res


def main():
    inputs = ["23 wed jan 2019", "355", "2"]
    curr_res = get_curr_results(*inputs)
    all_prev_res = get_prev_results(*inputs)

    for prev_res in all_prev_res:
        if compare_accu_res(curr_res, prev_res):
            prev_compile_res = compare_accu_res(
                curr_res, prev_res)

            for entry in prev_compile_res:
                print(entry)


if __name__ == "__main__":
    main()
