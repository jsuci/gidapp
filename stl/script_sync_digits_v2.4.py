import re
from itertools import *

"""
Using this script find patterns by collecting results by gap_value.
Print out the gap_value, time, common_digit, results, seq_type
"""


def get_gap_results(matches=2):
    """Gathers all gap results and returns a list of tuple
    containing the gap_value and time, results dictionary
    ex. [(2, {'11am': ['952', '517', '591'], '4pm': ['371',
    '976', '433'], '9pm': ['019', '928', '653']})...]
    """

    gap_results_list = []

    for gap_value in range(1, 200):
        with open("results_v2.txt", "r") as fo:
            last_entry = fo.readline().strip().split(" ")[-1]
            reversed_entries = list(islice(fo, 1, None))[::-1]
            to_skip = 0 if last_entry == "2" else 1
            step_value = gap_value + to_skip
            number_of_matches = 0
            gap_results = {"11am": [], "4pm": [], "9pm": []}

            for line_count, line_entry in enumerate(reversed_entries):
                date_results_list = re.split(r"\s{2,}", line_entry.strip())

                # Set number of matches here
                if line_count == step_value and number_of_matches != matches:
                    gap_results["11am"].append(date_results_list[1])
                    gap_results["4pm"].append(date_results_list[2])
                    gap_results["9pm"].append(date_results_list[3])

                    number_of_matches += 1
                    step_value += gap_value + 1

            gap_results_list.append((gap_value, gap_results))

    return gap_results_list


def diff_one(digit):
    return {
        0: 1,
        1: 2,
        2: 3,
        3: 4,
        4: 5,
        5: 6,
        6: 7,
        7: 8,
        8: 9,
        9: 0
    }[digit]


def diff_two(digit):
    return {
        0: 2,
        1: 3,
        2: 4,
        3: 5,
        4: 6,
        5: 7,
        6: 8,
        7: 9,
        8: 0,
        9: 1
    }[digit]


def seq_type(digits):
    """
    Given a sequence of string numbers ['8', '9', '0', '1'...] determine
    what type of sequence it has. Return a string of seq_type
        diff_one - if all numbers has a difference of 1
        diff_two - if all numbers has a difference of 2
        diff_zero - if all numbers has the same digit

        gap_one - all of the numbers has a difference of one except 1
            ex. 8, 9, 0, 1, 3 (2 missing)
                7, 9, 0, 1, 2 (8 missing)
    """

    uniq_digits = set([int(e) for e in digits])
    diff_one_count = 0
    diff_two_count = 0
    diff_none_count = 0

    if len(uniq_digits) == 1:
        return "diff_zero"
    elif len(uniq_digits) != len(digits):
        return "has_double"
    else:
        for digit in uniq_digits:

            if diff_one(digit) in uniq_digits:
                diff_one_count += 1
            elif diff_two(digit) in uniq_digits:
                diff_two_count += 1
            else:
                diff_none_count += 1

        # print(diff_one_count, diff_two_count, diff_none_count)

        # Filter diff_one
        if diff_two_count == 0 and diff_none_count < 2:
            return "diff_one"

        # Filter diff_two
        if (
            diff_one_count == 0 and
            diff_two_count >= 1 and
            diff_none_count != 2
        ):
            return "diff_two"

        # Filter gap_one
        if (
            diff_one_count != 0 and
            diff_two_count == 1 and
            diff_none_count != 2
        ):
            return "gap_one"


def get_seq_types(results, common=[]):
    """Given a list of results ['123', '345', '678'...] and a list of
    common digits (optional). Remove common digits from results and
    then determine their sequence type. Return a list of tuple
    containing the digits and seq_type [(('9', '9', '9'),
    'diff_zero')...]
    """

    trim_results = []

    if common:
        for result in results:
            for c in common:
                result = result.replace(c, "", 1)
            trim_results.append(result)
    else:
        trim_results = results

    output = []

    for seq in product(*trim_results):
        output_item = (seq, seq_type(seq))
        if seq_type(seq) and output_item not in output:
            output.append(output_item)

    return output


def has_common_digit(results):
    """Given a result check if it has a common_digit. Return a list
    of common digit.
    """
    common_digits = []

    for seq in product(*results):
        g = groupby(seq)
        if next(g, True) and not next(g, False):
            if seq[0] not in common_digits:
                common_digits.append(seq[0])

    return common_digits


def export_file(gap, time, common, results, seq_results):

    with open("results_sync_digits_v2.4.txt", "a") as fo:
        fo.write("gap: {}\n".format(gap))
        fo.write("time: {}\n".format(time))
        fo.write("common: {}\n".format(common))
        fo.write("results: {}\n".format(results))
        fo.write("seq_type:\n")
        for seq in seq_results:
            sequence, label = seq
            fo.write("{} <- {}\n".format(
                sequence, label))
        fo.write("\n\n")


def main():
    with open("results_sync_digits_v2.4.txt", "w") as fo:
        fo.write("")

    for item in get_gap_results(3):
        gap_value, gap_results = item

        for time, results in gap_results.items():
            common = has_common_digit(results)

            if common:
                seq_results = get_seq_types(results, common)

                print("gap: {}".format(gap_value))
                print("time: {}".format(time))
                print("common: {}".format(common))
                print("results: {}".format(results))
                print("seq_type: ")
                for seq in seq_results:
                    seq_digits, label = seq
                    print("{} <- {}".format(seq_digits, label))

                print("\n")

                export_file(gap_value, time, common, results,
                            seq_results)


if __name__ == "__main__":
    main()
