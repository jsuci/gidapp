import re
from itertools import *

"""
Possible combinations produced using this script is good for
2 to 3 days only
"""


def get_gap_results():
    """Gathers all gap results and returns a list of tuple
    containing the gap_value and time, results dictionary
    ex. [(2, {'11am': ['952', '517', '591'], '4pm': ['371',
    '976', '433'], '9pm': ['019', '928', '653']})...]
    """

    gap_results_list = []

    for gap_value in range(2, 20):
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
                if line_count == step_value and number_of_matches != 3:
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
    end = list_of_digits[-1]
    for digit in islice(list_of_digits, 1, None):
        if (digit - start) == 2:
            return str(start + 1)
        elif (start == 0 and digit == 1 and end == 8):
            return str(9)
        elif (start == 1 and digit == 2 and end == 9):
            return str(0)
        else:
            return None
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


def is_sync(results):
    """Given a list of results ex. ['358', '468', '827', ...]
    check if is in sync or not. By sync means it has:
        a. common_digit
        b. other digits must be in sequence (1, 2, 3.. or 3, 2, 1..)

    If all conditions are satisfied then output the following:
        a. common_digit
        b. common_results
        c. pair_sequence

    ex. [3, 4, 2] [5, 6, 7] [('38', '58'), ('48', '68'),
    ('28', '78')] 8
    """
    for i in range(10):
        common_digit = str(i)
        has_common_digit = True
        pairs_list = []
        common_results = []

        for result in results:
            if common_digit not in result:
                has_common_digit = False
            else:
                join_result = " ".join([
                    "({})".format(e) if e == common_digit else
                    " {} ".format(e) for e in result])

                common_results.append(join_result)
                pairs_list.append(result.replace(common_digit, "", 1))

        if has_common_digit:
            """After you have identified results that has common
            digits you can now further filter the results by choosing
            wether the other digits is in sequence or has a
            gap of 2
            """

            pair_sequence = []
            possible_digits = [common_digit]

            """From the list of pairs in pairs_list make all possible
            combinations of pairs
            """
            for pair_digit in product(*pairs_list):

                """Filter pair_digit if is in sequence or has gap:
                    1 - if all digits are in sequence
                    2 - if digits has a gap of 2
                """
                if (is_sequence(pair_digit) == 1 and
                        pair_digit not in pair_sequence):

                    """For output purposes only. After the common_digit
                    has been remove show the pairs of previous result
                    """
                    pair_digit_join = "".join(pair_digit)
                    pair_sequence.append(pair_digit_join)

                    """IMPORTANT: this will decide the possible
                    combinations base on the previous is_sequence(
                    pair_digit) filter
                    """
                    possible_digits.append(get_next_digit(pair_digit))

            """For a complete sequence of digits limit the number of
            pair_sequence to 2. 1 if at least 1 pair_sequence
            """
            if len(pair_sequence) == 2:
                """Only select pair_sequence that are unique and no
                repeating digits ex. ['7', '8', '9'] and ['2', '3','4']
                """

                has_repeat_pair_digit = False

                for digit in pair_sequence[0]:
                    if digit in pair_sequence[1]:
                        has_repeat_pair_digit = True

                if not has_repeat_pair_digit:
                    possible_combi = ["".join(e) for e in product(
                        *possible_digits)]

                    return (common_digit, common_results,
                            pair_sequence, possible_combi)


def main():
    for item in get_gap_results():
        gap_value, gap_results = item
        for time, results in gap_results.items():
            if is_sync(results):
                common, filter_res, sequence, combi = is_sync(results)
                print("gap: {}\ntime: {}".format(gap_value, time))
                print("common: {}\ncombi: {}".format(common, combi))
                print("seq: {}".format(sequence))
                print("results: ")
                for entry in filter_res:
                    print(entry)

                print("\n")


if __name__ == "__main__":
    main()
