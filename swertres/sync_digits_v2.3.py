"""
FIXED: Fix the way the script determines if it is in_sequence
or not. Separating the digits in to left and right digit is not
the proper way since there are sequences that are left out
ex.
    [0, 5]
    [3, 1]
    [2, 6]
The above sample when using left and right digit would turn out to
be left = [0, 3, 2] which is not a diff_one sequence but there is a
[0, 1, 2] and at the same time a diff_two sequence at [5, 3, 6] and
[5, 3, 2]


FIXED: Change the way the script determine if it has a common_digit or
not.
"""

import re
from itertools import *

"""
HOW TO USE 1: This script will filter out result base on diff_one,
diff_two and common_digits. It will also produce possible combinations
for base on the given filter. Filters out first 100 results with
matches of 3. You must enter manually the time ex. '11am', '4pm', '9pm'


HOW TO USE 2: You can use this script to filter out diff_one_one.
diff_one_one filters out this pattern:

(04)(09)done 049
(02)(08)done 280
(03)(07)done 730
(05)(06)done 605 <- result

1. To spot this kind of pattern and predict the next result, first is
to set the get_gap_results matches to "3"
2. Record the time, and expected date of diff_one_one results to comeout ex.
    // previous result; macthes: 3
    gap: 34
    time: 11am
    status: diff_one_one
    diffs: ([['1', '5']], [])
    common: ['9']
    combi: ['91', '95']
    results:
     8  3 (9)
    (9) 3  2
    (9)(9) 4

    // predicted results; matches: 4
    gap: 34
    time: 11am
    status: diff_one_two
    diffs: ([['1', '6'], ['0', '5']], [])
    common: ['9']
    combi: ['910', '915', '960', '965']
    results:
     5 (9) 1 <- (confirmed result!)
     8  3 (9)
    (9) 3  2
    (9)(9) 4

"""


def get_gap_results():
    """Gathers all gap results and returns a list of tuple
    containing the gap_value and time, results dictionary
    ex. [(2, {'11am': ['952', '517', '591'], '4pm': ['371',
    '976', '433'], '9pm': ['019', '928', '653']})...]
    """

    gap_results_list = []

    for gap_value in range(2, 100):
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
                if line_count == step_value and number_of_matches != 2:
                    gap_results["11am"].append(date_results_list[1])
                    gap_results["4pm"].append(date_results_list[2])
                    gap_results["9pm"].append(date_results_list[3])

                    number_of_matches += 1
                    step_value += gap_value + 1

            gap_results_list.append((gap_value, gap_results))

    return gap_results_list


def get_next_digit(list_of_digits):
    """Given a list of string digits ('1', '2', '3') or ['1', '2', 3]
    get their start and end digits and then subtract or add to get the
    next digit. Returns a list of subtracted and added values
    """

    list_of_digits = [int(e) for e in list_of_digits]
    list_of_digits.sort()
    start = list_of_digits[0]
    end = list_of_digits[-1]

    results = [str(0) if end + 1 == 10 else str(end + 1),
               str(9) if start - 1 == -1 else str(start - 1)]

    return sorted(results)


def get_in_between_digit(list_of_digits):
    """Given a list of string digits ('5', '3') or ['6', '8']
    get their start and end digits and if there difference is
    2 then get their in between value
    """

    list_of_digits = [int(e) for e in list_of_digits]
    list_of_digits.sort()

    start = list_of_digits[0]
    first = list_of_digits[0]
    end = list_of_digits[-1]
    for digit in islice(list_of_digits, 1, None):

        if (digit - start) == 2:
            return str(start + 1)
        elif (first == 0) and (end == 8):
            return str(9)
        elif (first == 1) and (end == 9):
            return str(0)
        else:
            start = digit


def is_sequence(list_of_digits):
    """Given a list of unsorted string digits ex. ['4', '8'..]
    from 0 to 9 of any given length, check if all the values fit the
    conditions below:
        if all digits has a difference of 1 then return 1
        if some digits are in sequence and the other digit has
        a difference of of 2 then return 2
        else return 0
    """
    list_of_digits = [int(e) for e in list_of_digits]
    list_of_digits.sort()
    start = list_of_digits[0]
    first_digit = list_of_digits[0]
    last_digit = list_of_digits[-1]
    diff_not_one = []

    for digit in islice(list_of_digits, 1, None):
        if abs(start - digit) != 1:
            diff_not_one.append(abs(start - digit))

        start = digit

    diff_not_one.sort()

    len_diff_not_one = len(diff_not_one)

    if not len_diff_not_one:
        return 1
    else:
        if first_digit == 0 and last_digit == 9:
            if len_diff_not_one == 1:
                if diff_not_one[0] == 2:
                    return 2
                else:
                    return 1
            elif (
                len_diff_not_one == 2 and
                diff_not_one[0] == 2 and
                diff_not_one[1] != 2
            ):
                return 2
            else:
                return 0
        elif first_digit == 0 and last_digit == 8:
            if len_diff_not_one == 1:
                return 2
            else:
                return 0
        else:
            if len_diff_not_one == 1 and diff_not_one[0] == 2:
                return 2
            else:
                return 0


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


def possible_digits(results, common):
    seq = []
    diff_one = []
    diff_two = []
    possible = []
    status = ""

    # Strip common digits to get pairs
    for result in results:
        temp = result
        for digit in common:
            temp = temp.replace(digit, "", 1)
        seq.append(temp)

    # Classify pairs into diff_one or diff_two
    for digits in product(*seq):
        if is_sequence(digits) == 1:
            diff_one_digits = get_next_digit(digits)

            if diff_one_digits not in diff_one:
                diff_one.append(diff_one_digits)
        elif is_sequence(digits) == 2:
            diff_two_digits = get_in_between_digit(digits)

            if diff_two_digits not in diff_two:
                diff_two.append(diff_two_digits)
        else:
            pass

    # Filter options
    if len(common) == 2 and (diff_one or diff_two):
        status = "two_common"
        diff_one_two = diff_one if diff_one else diff_two
        for combi in product(*common, *diff_one_two):
            combi = "".join(combi)
            possible.append(combi)

    if len(common) == 1:
        if diff_one and diff_two:
            status = "diff_one_and_two"
            for combi in product(common, chain(*diff_one), diff_two):
                combi = "".join(combi)
                possible.append(combi)

        elif diff_one and len(diff_one) == 2:
            status = "diff_one_two"
            for combi in product(common, *diff_one):
                combi = "".join(combi)
                possible.append(combi)

        elif diff_one and len(diff_one) == 1:
            status = "diff_one_one"
            for combi in product(*common, *diff_one[0]):
                combi = "".join(combi)
                possible.append(combi)

        elif diff_two and len(diff_two) == 2:
            status = "diff_two_only"
            diff_two_pairs = ["".join(e) for e in combinations(
                diff_two, 2)]
            for combi in product(common, diff_two_pairs):
                combi = "".join(combi)
                possible.append(combi)
        else:
            pass

    diffs = (diff_one, diff_two)

    return (possible, status, diffs)


def format_results(results, common):
    final_output = []

    for result in results:
        for digit in result:
            format_result = [
                "({})".format(e) if e in common else
                " {} ".format(e) for e in result
            ]

        final_output.append("".join(format_result))

    return final_output


def is_sync(results):
    """Given a list of results ex. ['358', '468', '827', ...]
    check if is in sync or not. By sync means it has:
        a. common_digit
        b. other digits must be in sequence (1, 2, 3.. or 3, 2, 1..)

    If all conditions are satisfied then output the following:
        a. common_digit
        b. format_res
        c. combis

    ex. [3, 4, 2] [5, 6, 7] [('38', '58'), ('48', '68'),
    ('28', '78')] 8
    """

    common_digits = has_common_digit(results)

    if common_digits:
        """After you have identified results that has common
        digits you can now further filter the results by choosing
        wether the pairs is in sequence or has a gap of 2
        """
        combis, status, diffs = possible_digits(results, common_digits)

        if status:
            format_res = format_results(results, common_digits)
            output = (common_digits, format_res, combis, status, diffs)

            return output


def export_file(results, time, gap_value):

    common, format_res, combi, status, diffs = is_sync(results)

    with open("results_sync_digits_v2.3.txt", "a") as fo:
        fo.write("gap: {}\n".format(gap_value))
        fo.write("time: {}\n".format(time))
        fo.write("status: {}\n".format(status))
        fo.write("diffs: {}\n".format(diffs))
        fo.write("common: {}\n".format(common))
        fo.write("combi: {}\n".format(combi))
        fo.write("results: \n")
        for entry in format_res:
            fo.write("{}\n".format(entry))

        fo.write("\n\n")


def main():
    with open("results_sync_digits_v2.3.txt", "w") as fo:
        fo.write("")

    # option_time = input("Enter time (11am, 4pm or 9pm): ")
    option_time = "11am"

    for item in get_gap_results():
        gap_value, gap_results = item
        for time, results in gap_results.items():
            if is_sync(results) and time == option_time:

                export_file(results, time, gap_value)

                common, format_res, combi, status, diffs = is_sync(results)
                print("gap: {}".format(gap_value))
                print("time: {}".format(time))
                print("status: {}".format(status))
                print("diffs: {}".format(diffs))
                print("common: {}".format(common))
                print("combi: {}".format(combi))
                print("results: ")
                for entry in format_res:
                    print(entry)

                print("\n")


if __name__ == "__main__":
    main()
