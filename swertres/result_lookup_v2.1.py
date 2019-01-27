"""
Given a digit to search and its current location search all
previous result and output the first three previous result of
that digit.
"""


from timeit import *
from itertools import *
import re


def get_last_result():
    """Get the last result and return a string of digit"""
    with open("results_v2.txt") as fi:
        last_result = list(fi)[-1].split(" ")[-1].strip()

        return last_result


def get_last_two_results():
    """Get the last result and return a list of digit"""
    with open("results_v2.txt") as fi:
        entries = [re.split(r"\s{10}", e.strip()) for e in fi]
        last_result = []

        if len(entries[-1]) == 4:
            last_result.extend(entries[-2][1:])
            last_result.extend(entries[-1][1:])
        else:
            last_result.extend(entries[-3][1:])
            last_result.extend(entries[-2][1:])

        return last_result


def get_combinations(digits):
    combi = []

    for permute in permutations(digits, 3):

        # # Limit permutations
        # if digits[0] == permute[0]:
        #     combi.append("".join(permute))

        # Generate all possible permutations
        combi.append("".join(permute))

    return combi


def compare_digits(digit_one, digit_two):
    compare_count = 0

    for j in set(digit_one):
        if j in set(digit_two):
            compare_count += 1

    # Set to >= 2 for is_pair() and == 3 for has_common()
    if compare_count == 3:
        return True
    else:
        return False


def search_results(digits, exact_loc=0):
    with open("results_v2.txt", "r") as fi:
        entries = [re.split(r"\s{10}", e.strip()) for e in fi]
        index = 0

        while index < (len(entries) - 1):

            if digits in entries[index]:

                # Get the position of the focus digit
                curr_res_loc = entries[index].index(digits)

                prev_res = entries[index - 1]
                curr_res = entries[index]
                next_res = entries[index + 1]
                accu_entries = (prev_res, curr_res, next_res)

                filtered_res = exact_location(
                    accu_entries, curr_res_loc, exact_loc)
                # filtered_res = is_pair(accu_entries, curr_res_loc)
                # filtered_res = has_common(accu_entries, curr_res_loc)

                if filtered_res:
                    for e in filtered_res:
                        print(e)

                    print("\n")

            index += 1


def is_pair(accu_res, digit_loc):
    """Given accu_res(tuple consisting prev, curr, nxt results)
    and digit_loc(index in which the given digit was found) check
    if the top digit and bottom digit has at least 2 same digits.
    Return filtered results.
    """

    prev, curr, nxt = accu_res
    is_pair_count = False

    # compare_digits() controls the number of
    # successful comparisons
    if len(nxt) != 3 and compare_digits(
            prev[digit_loc], nxt[digit_loc]):
        is_pair_count = True

    if is_pair_count:
        return accu_res


def has_common(accu_res, digit_loc):
    """Filter accu_res using the last two lines of the current
    results. If the last_tow_results contains at least 2 digits
    in accu_res then return that accu_res
    """

    prev, curr, nxt = accu_res
    chain_res = [e for e in chain(prev[1:], curr[1:], nxt[1:])]
    res_to_compare = get_last_two_results()
    compare_count = 0

    for digit_one in res_to_compare:
        for digit_two in chain_res:
            if compare_digits(digit_one, digit_two):
                compare_count += 1

    if compare_count == 2:
        return accu_res


def no_filter(accu_res, digit_loc):
    return accu_res


def exact_location(accu_res, digit_loc, exact_loc):
    if digit_loc == exact_loc:
        return has_common(accu_res, digit_loc)


def main():
    for digits in get_combinations('150'):
        search_results(digits, exact_loc=3)


if __name__ == "__main__":
    main()
