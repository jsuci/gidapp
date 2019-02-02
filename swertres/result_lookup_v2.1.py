"""
Given a digit and its current location search all
previous result and output the previous result
"""


from timeit import *
from itertools import *
import re


def get_combinations(digits):
    combi = []

    for permute in permutations(digits, 3):

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


def search_results(digits, exact_loc):
    """
    Input: Given a number and its location, search through previous
    results that has same digit combination and location.
    # Search through previous result.index

    Output: A list of result that matches the condition
    """

    # Scan through all the results
    # Check each entries if it has the digit and the position is exact
    # Make a list of matches

    matches = []
    for num_combi in get_combinations(digits):
        with open("results_v2.txt", "r") as fi:
            entries = [re.split(r"\s{2,}", e.strip()) for e in fi]
            index = 0

            while index < len(entries):
                if num_combi in entries[index]:

                    # Get the position of the focus digit
                    curr_res_loc = entries[index].index(num_combi)

                    if (exact_loc == curr_res_loc and
                            entries[index] not in matches):
                        matches.append(entries[index])

                index += 1

    return matches


def main():
    for entry in search_results("614", 3):
        print(entry)


if __name__ == "__main__":
    main()
