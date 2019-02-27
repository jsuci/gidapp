from itertools import *
import re

"""
Process results_v2.txt and look for digits that match
the current result and position
"""

def compare_digits(digit_1, digit_2):

    for num_1 in digit_1:
        if num_1 in digit_2:
            digit_2 = digit_2.replace(num_1, "", 1)

    if len(digit_2) == 0:
        return True
    else:
        return False


def filter_results(curr_result, time):

    accu_result = []

    with open("results_v2.txt", "r") as fi:
        for entry in islice(fi, 2, None):
            entry = re.split(r"\s{2,}", entry.strip())
            date = entry[0]
            results = entry[1:]

            for count, result in enumerate(results):
                if (
                    compare_digits(curr_result, result) and
                    count == time
                ):
                    accu_result.append((date, count, results))

    return accu_result


def main():
    # The current result
    curr_res = "697"

    # Time, 0 for 11am, 1 for 4pm and 2 for 9pm
    time = 0

    for entry in filter_results(curr_res, time):
        print(entry)




if __name__ == "__main__":
    main()