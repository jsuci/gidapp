from itertools import *
from re import *
from pprint import *
from datetime import *
from fileinput import *


def get_generated_date_v1():
    """Get current date from updated string of
    results_v2.txt. Return a string of date
    """

    with open("results_v1.txt") as fi:
        date = fi.readline().strip().replace("updated: ", "")

    return date


def is_current_date():
    """Get results_v2.txt current date and compare it to
    results_common_v2.1.txt date. Return True if they
    are the same and False if not
    """

    with open("results_count_missing_v1.1.txt", "r") as fo:
        fi_date = "updated: " + get_generated_date_v1()
        fo_date = fo.readline().strip()

        if fi_date != fo_date:
            return fi_date


def get_reverse_result():
    results = []
    with open("results_v1.txt", "r") as fi:
        for entry in islice(fi, 2, None):
            result = entry.strip()
            results.insert(0, result)

    return results


def count_missing_digit(digit):
    """Given a str digit determine the longest missing
    position of that digit. Return a list containing
    digit, {position: missing_count}, "0 _ _")
    """

    results = get_reverse_result()
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


def export_results(sorted_missing):

    with open("results_count_missing_v1.1.txt", "a") as fo:
        fo.write("DATE GENERATED: {}\n".format(get_generated_date_v1()))
        for entry in sorted_missing:
            fo.write("{} <- {:2}\t\t{}\n".format(
                entry[0],
                entry[2],
                entry[3]))

        fo.write("\n\n")

    with input("results_count_missing_v1.1.txt", inplace=True) as fio:
        for entry in fio:
            if "updated:" in entry:
                print(is_current_date())
            else:
                print(entry, end="")


def all_missing_digit():
    all_missing = []

    for i in range(10):
        all_missing.append(
            count_missing_digit(str(i)))

    sorted_missing = sorted(
        all_missing, key=(lambda x: x[2]), reverse=True)

    for entry in sorted_missing:
        print("{} <- {:2}\t\t{}".format(
            entry[0],
            entry[2],
            entry[3]))

    print("\n\n")

    if is_current_date():
        export_results(sorted_missing)


def main():
    all_missing_digit()


if __name__ == "__main__":
    main()
