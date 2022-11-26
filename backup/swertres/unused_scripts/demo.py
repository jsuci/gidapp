from itertools import *
from re import *
from pprint import *
from datetime import *


def get_reverse_results_v2():
    """Given all the results from results_v2.txt
    return a dictionary containing time results
    in this format

    {"11am": ['123', ...], "4pm": ['456', ...]..}
    """

    reverse = []
    time_results = {}

    with open("results_v2.txt", "r") as fi:
        for entry in islice(fi, 2, None):
            entry = entry.strip()
            reverse.insert(0, entry)

    for r_entry in reverse:
        results = split(r"\s{2,}", r_entry)[1:]
        if len(results) == 3:
            time_results.setdefault("11am", [])
            time_results.setdefault("4pm", [])
            time_results.setdefault("9pm", [])

            time_results["11am"].append(results[0])
            time_results["4pm"].append(results[1])
            time_results["9pm"].append(results[2])

    return time_results


def count_missing_digit(results, digit):
    """Given a str digit determine the longest missing
    position of that digit. Return a list containing
    digit, {position: missing_count}, "0 _ _")
    """

    digit = str(digit)
    first_count = 0
    second_count = 0
    third_count = 0
    highest_count = 0
    highest_format = ""

    final_result = [digit, {"first": 0, "second": 0, "third": 0}]

    for result in results:
        if digit != result[0]:
            first_count += 1
        else:
            final_result[1]["first"] = first_count
            if highest_count < first_count:
                highest_count = first_count
                highest_format = "{} - -".format(digit)
            break

    for result in results:
        if digit != result[1]:
            second_count += 1
        else:
            final_result[1]["second"] = second_count
            if highest_count < second_count:
                highest_count = second_count
                highest_format = "- {} -".format(digit)
            break

    for result in results:
        if digit != result[2]:
            third_count += 1
        else:
            final_result[1]["third"] = third_count
            if highest_count < third_count:
                highest_count = third_count
                highest_format = "- - {}".format(digit)
            break

    final_result.extend([highest_count, highest_format])
    return final_result


def main():
    for time, results in get_reverse_results_v2().items():

        print(time)

        all_missing = []
        for digit in range(0, 10):
            all_missing.append(
                count_missing_digit(results, digit))

        sorted_missing = sorted(
            all_missing, key=(lambda x: x[2]), reverse=True)

        for entry in sorted_missing:
            print("{} <- {:2}\t\t{}".format(
                entry[0],
                entry[2],
                entry[3]))

        print("\n")


if __name__ == "__main__":
    main()
