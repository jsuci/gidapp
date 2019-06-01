from itertools import *
from re import *
from pprint import *
from datetime import *
from fileinput import *


def get_reverse_result():
    results = []
    with open("results_v1.txt", "r") as fi:
        for entry in islice(fi, 2, None):
            result = entry.strip()
            results.insert(0, result)

    return results


def count_missing_digit(results, digit):
    """Given a str digit determine the longest missing
    position of that digit. Return a list containing
    digit, {position: missing_count}, "0 _ _")
    """

    # results = get_reverse_result()
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


def result_gap():
    """Given two different date time strings, count how
    many results have gone by. Return an integer value"""

    ((prev_date, prev_int),
        (curr_date, curr_int)) = date_gap()

    multiplier = 3
    time_diff = (curr_date - prev_date).days

    endpoints = (
        multiplier - (prev_int + 1) +
        (curr_int + 1)
    )

    if time_diff != 1:
        return (time_diff - 1) * multiplier + endpoints
    else:
        return endpoints


def date_gap():
    """Return a list of tuple containing date object and an int value
    taken from results_v1.txt and results_count_missing_v1.1.txt"""

    with open("results_count_missing_v1.1.txt", "r") as f1:
        prev_dt = f1.readline().strip().replace("updated: ", "")

    with open("results_v1.txt", "r") as f2:
        curr_dt = f2.readline().strip().replace("updated: ", "")

    prev_date, prev_int = [prev_dt[:-2], int(prev_dt[-1:])]
    curr_date, curr_int = [curr_dt[:-2], int(curr_dt[-1:])]

    prev_date = datetime.strptime(prev_date, "%d %a %b %Y")
    curr_date = datetime.strptime(curr_date, "%d %a %b %Y")

    return [(prev_date, prev_int), (curr_date, curr_int)]


def all_missing_digit():

    with open("results_count_missing_v1.1.txt", "a") as fo:

        ((prev_date, prev_int),
            (curr_date, curr_int)) = date_gap()

        for i in reversed(range(result_gap())):
            results = get_reverse_result()[i:]
            all_missing = []

            for i in range(10):
                all_missing.append(
                    count_missing_digit(results, str(i)))

            if prev_int == 2:
                prev_date += timedelta(days=1)
                prev_int = 0

            else:
                prev_int += 1

            print("DATE GENERATED: {} {}".format(
                prev_date.strftime("%d %a %b %Y"), prev_int))
            print("RESULT: {}".format(results[0]))

            fo.write("DATE GENERATED: {} {}\n".format(
                prev_date.strftime("%d %a %b %Y"), prev_int))
            fo.write("RESULT: {}\n".format(results[0]))

            sorted_missing = sorted(
                all_missing, key=(lambda x: x[2]), reverse=True)

            for entry in sorted_missing:
                print("{} <- {:2}\t\t{}".format(
                    entry[0],
                    entry[2],
                    entry[3])
                )

                fo.write("{} <- {:2}\t\t{}\n".format(
                    entry[0],
                    entry[2],
                    entry[3])
                )

            print("\n\n")
            fo.write("\n\n")

    with input("results_count_missing_v1.1.txt", inplace=True) as fio:
        for entry in fio:
            if "updated:" in entry:
                print("updated: {} {}".format(
                    curr_date.strftime("%d %a %b %Y"), curr_int))
            else:
                print(entry, end="")


def main():
    all_missing_digit()


if __name__ == "__main__":
    main()
