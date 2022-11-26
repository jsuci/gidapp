"""
Every gap results follows a sequence pattern
ex:
11am (diff_one)
8 7 (4)
5 4 (6)
9 8 (5)

9pm (diff_two)
1 (6) 7
1 (7) 1
7 (5) 7

diff_two is a typr of sequence where in there is
a difference of two in the seq.
ex. 57->(6), 1235->(4)

diff_one is a type of sequence where in there is
a difference of one
ex. 12, 1234

gap_results it is the gap between results
ex. gap_result of 1 means
24 thu jan 2019       305       687       173 <- 1 gap
25 fri jan 2019       888       953       902
26 sat jan 2019       069       673       225 <- 1 gap
27 sun jan 2019       882       451       287

match_count is the number of matches
ex. gap_result of 1 and match_count of 3 means
22 tue jan 2019       924       820       614 <- 3 match_count
23 wed jan 2019       552       355       150
24 thu jan 2019       305       687       173 <- 2 match_count
25 fri jan 2019       888       953       902
26 sat jan 2019       069       673       225 <- 1 match_count
27 sun jan 2019       882       451       287

This script will try to do the following:
1. gather all results

2. compile them in a list of tuple containing the gap_value
a dictionary of time results. Results change in number of entries
depoending on the match count
ex. [(gap_val, {"time": [results]}),...]

3. start the filtering process and when it is done print the possible
combinations for 11am, 4pm and 5pm
"""


import re
from itertools import *


def get_gap_results(match_count):
    final_accu_res = []

    for gap_value in range(1, 20):
        with open("results_v2.txt", "r") as fi:

            # Turn to list and reverse it
            entries = [re.split(r"\s{2,}", e.strip())
                       for e in fi][::-1]

            # Control the number of matches
            num_matches = 0

            # Add one to step_count if results are not finished yet
            to_skip = 0 if len(entries[0]) == 4 else 1
            step_count = gap_value + to_skip

            temp_accu_res = {"11am": [], "4pm": [], "9pm": []}

            for count, entry in enumerate(entries):
                if (count == step_count and
                        num_matches != match_count):

                    temp_accu_res["11am"].append(entry[1])
                    temp_accu_res["4pm"].append(entry[2])
                    temp_accu_res["9pm"].append(entry[3])

                    step_count += gap_value + 1
                    num_matches += 1

            final_accu_res.append((gap_value, temp_accu_res))

    return final_accu_res


def get_seq_type(list_of_digits):
    """Given a list of unsorted integers ex. [4, 8, 3, ...] from
    0 to 9 of any given length, check if all the values fit the
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


def get_all_results():
    all_results = []
    for match_count in range(3, 9):
        for entry in get_gap_results(match_count):
            all_results.append(entry)

    return all_results


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

        # 0 and 8 has a gap of 2 and
        # 1 and 9 has a gap of 2
        elif (first == 0) and (end == 8):
            return str(9)
        elif (first == 1) and (end == 9):
            return str(0)
        else:
            start = digit


def get_position(result_collection):
    """Given a list of tuple containing an int(gap_value)
    and dictionary of results {"11am": ['123', ...]}
    classify the possible digits and formulate new possible
    pairs
    """
    eleven_am = {"first": set(), "second": set(), "third": set()}
    four_pm = {"first": set(), "second": set(), "third": set()}
    nine_pm = {"first": set(), "second": set(), "third": set()}

    final_pair_results = {"11am": [], "4pm": [], "9pm": []}

    for entry in result_collection:
        gap_value, results = entry

        for time, list_res in results.items():
            if mark_positions(list_res):
                index, marked_res, poss_val = mark_positions(
                    list_res)

                if time == "11am":
                    if index[0] == 1:
                        eleven_am["first"].add(poss_val[0])

                    if index[0] == 2:
                        eleven_am["second"].add(poss_val[0])

                    if index[0] == 3:
                        eleven_am["third"].add(poss_val[0])

                elif time == "4pm":
                    if index[0] == 1:
                        four_pm["first"].add(poss_val[0])

                    if index[0] == 2:
                        four_pm["second"].add(poss_val[0])

                    if index[0] == 3:
                        four_pm["third"].add(poss_val[0])

                else:
                    if index[0] == 1:
                        nine_pm["first"].add(poss_val[0])

                    if index[0] == 2:
                        nine_pm["second"].add(poss_val[0])

                    if index[0] == 3:
                        nine_pm["third"].add(poss_val[0])

    # 3 digit combinations
    # 11am
    for pair_combi in product(eleven_am["first"],
                              eleven_am["second"], eleven_am["third"]):
        pair_combi_format = "".join(pair_combi)
        final_pair_results["11am"].append(pair_combi_format)

    # 4pm
    for pair_combi in product(four_pm["first"],
                              four_pm["second"], four_pm["third"]):
        pair_combi_format = "".join(pair_combi)
        final_pair_results["4pm"].append(pair_combi_format)

    # 9pm
    for pair_combi in product(nine_pm["first"],
                              nine_pm["second"], nine_pm["third"]):
        pair_combi_format = "".join(pair_combi)
        final_pair_results["9pm"].append(pair_combi_format)

    # # 2 digit pair combiantions
    # # 11am
    # for pair_combi in product(eleven_am["first"], eleven_am["second"]):
    #     pair_combi_format = "{}{}-".format(
    #         pair_combi[0], pair_combi[1])
    #     final_pair_results["11am"].append(pair_combi_format)

    # for pair_combi in product(eleven_am["first"], eleven_am["third"]):
    #     pair_combi_format = "{}-{}".format(
    #         pair_combi[0], pair_combi[1])
    #     final_pair_results["11am"].append(pair_combi_format)

    # for pair_combi in product(eleven_am["second"], eleven_am["third"]):
    #     pair_combi_format = "-{}{}".format(
    #         pair_combi[0], pair_combi[1])
    #     final_pair_results["11am"].append(pair_combi_format)

    # # 4pm
    # for pair_combi in product(four_pm["first"], four_pm["second"]):
    #     pair_combi_format = "{}{}-".format(
    #         pair_combi[0], pair_combi[1])
    #     final_pair_results["4pm"].append(pair_combi_format)

    # for pair_combi in product(four_pm["first"], four_pm["third"]):
    #     pair_combi_format = "{}-{}".format(
    #         pair_combi[0], pair_combi[1])
    #     final_pair_results["4pm"].append(pair_combi_format)

    # for pair_combi in product(four_pm["second"], four_pm["third"]):
    #     pair_combi_format = "-{}{}".format(
    #         pair_combi[0], pair_combi[1])
    #     final_pair_results["4pm"].append(pair_combi_format)

    # # 9pm
    # for pair_combi in product(nine_pm["first"], nine_pm["second"]):
    #     pair_combi_format = "{}{}-".format(
    #         pair_combi[0], pair_combi[1])
    #     final_pair_results["4pm"].append(pair_combi_format)

    # for pair_combi in product(nine_pm["first"], nine_pm["third"]):
    #     pair_combi_format = "{}-{}".format(
    #         pair_combi[0], pair_combi[1])
    #     final_pair_results["4pm"].append(pair_combi_format)

    # for pair_combi in product(nine_pm["second"], nine_pm["third"]):
    #     pair_combi_format = "-{}{}".format(
    #         pair_combi[0], pair_combi[1])
    #     final_pair_results["9pm"].append(pair_combi_format)

    return final_pair_results


def mark_positions(list_results):
    """Given a list of results ["234", "456", "789", ...]
    identify which position has sequence and mark them with
    "()" accordingly. Return a tuple containing the number
    of identified positions, [1] if its location is 1 and if
    there are two in a digit then return a list of positions
    [1, 3], a list of marked_results ['3 0 (5)', ...] and
    possible digit [6]
    """

    first_pos = []
    second_pos = []
    third_pos = []

    for result in list_results:
        first_pos.append(result[0])
        second_pos.append(result[1])
        third_pos.append(result[2])

    first_seq = get_seq_type(first_pos)
    second_seq = get_seq_type(second_pos)
    third_seq = get_seq_type(third_pos)

    first_pos_digit = get_in_between_digit(first_pos)
    second_pos_digit = get_in_between_digit(second_pos)
    third_pos_digit = get_in_between_digit(third_pos)

    # Set first_seq, second_seq, third_seq to 1 if you want
    # to filter results with gap of 1. If not then set it to 2
    if (first_seq == 2) and (second_seq == 2) and (third_seq == 2):
        all_format = ["({}) ({}) ({})".format(
            x[0], x[1], x[2]) for x in list_results]

        return ([1, 2, 3], all_format,
                [first_pos_digit, second_pos_digit, third_pos_digit])

    elif (first_seq == 2) and (third_seq == 2):
        first_third_format = ["({}) {} ({})".format(
            x[0], x[1], x[2]) for x in list_results]

        return ([1, 3], first_third_format,
                [first_pos_digit, third_pos_digit])

    elif (first_seq == 2) and (second_seq == 2):
        first_second_format = ["({}) ({}) {}".format(
            x[0], x[1], x[2]) for x in list_results]

        return ([1, 2], first_second_format,
                [first_pos_digit, second_pos_digit])

    elif first_seq == 2:
        first_pos_format = ["({}) {} {}".format(
            x[0], x[1], x[2]) for x in list_results]

        return ([1], first_pos_format, [first_pos_digit])

    elif second_seq == 2:
        second_post_format = ["{} ({}) {}".format(
            x[0], x[1], x[2]) for x in list_results]

        return ([2], second_post_format, [second_pos_digit])

    elif third_seq == 2:
        third_post_format = ["{} {} ({})".format(
            x[0], x[1], x[2]) for x in list_results]

        return ([3], third_post_format, [third_pos_digit])

    else:
        return None


def main():
    result_collection = get_all_results()
    for key, values in get_position(result_collection).items():
        print(key, sorted(values))
        print("\n")


if __name__ == "__main__":
    main()
