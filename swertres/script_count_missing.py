from itertools import *


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


def main():
    all_missing_digit()


if __name__ == "__main__":
    main()
