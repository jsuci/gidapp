"""
Given a list of results ['730', '280', '049'] determine
their common, digit and their seq_types
"""

from itertools import *


def common_digits(results):
    """Given a list of results check ['730', '280', '049']
    if it has a common_digit. Return a list of common digit.
    """
    common_digits = []

    for seq in product(*results):
        g = groupby(seq)
        if next(g, True) and not next(g, False):
            if seq[0] not in common_digits:
                common_digits.append(seq[0])

    return common_digits


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


def get_seq_types(results):
    """Given a list of results ['123', '345', '678'...] and a list of
    common digits ['0', '1'](optional). Determine the seq_type of all
    the digits and return a dictionary containing the digits and
    seq_type count

    ex.
    {
        'diff_one': {'count': 2, 'results': [('7', '8', '9'), ...]},
        'diff_two': {'count': 0, 'results': []},
        'diff_zero': {'count': 0, 'results': []},
        'gap_one': {'count': 0, 'results': []}
    }
    """

    trim_results = []
    seq_type_results = {}
    common = common_digits(results)
    seq_type_results.setdefault("common", [])

    if common:
        seq_type_results["common"].extend(common)
        for result in results:
            for c in common:
                result = result.replace(c, "", 1)
            trim_results.append(result)
    else:
        trim_results = results

    for seq in product(*trim_results):
        if seq_type(seq):
            seq_type_results.setdefault(
                seq_type(seq), [])

            if seq not in seq_type_results[seq_type(seq)]:
                seq_type_results[seq_type(seq)].append(seq)

    return seq_type_results


def get_reverse_results_v1():
    """Get reverse results for results_v1.txt"""

    results = []

    with open("results_v1.txt", "r") as fi:
        for entry in islice(fi, 2, None):
            result = entry.strip()
            results.insert(0, result)

    return results


def get_gap_results_v1():
    """Get reverse results for results_v1.txt"""

    results = get_reverse_results_v1()
    gap_results = {}
    for gap in range(1, 20):
        step = gap
        temp_results = []

        for count, result in enumerate(results):

            # Control the number of results here
            if step == count and len(temp_results) != 2:
                temp_results.append(result)

                step += (gap + 1)

        gap_results.setdefault(gap, temp_results)

    return gap_results


def total_seq(res, sequence):
    """Given a list of results and a list of tuple
    containing sequence of digits. Check if all the
    sequence are consumed. Return True if they are
    and False if not
    """

    for seq in sequence:
        for index, d_seq in enumerate(seq):
            if d_seq in res[index]:
                res[index] = res[index].replace(d_seq, "", 1)

    if len(set(res)) == 1:
        return True
    else:
        return False


def main():
    for gap, results in get_gap_results_v1().items():
        seq_results = get_seq_types(results)

        if (
            "common" in seq_results and
            len(seq_results["common"]) == 1 and
            "diff_two" in seq_results and
            len(seq_results["diff_two"]) >= 2 and
            "diff_one" in seq_results and
            len(seq_results["diff_one"])
        ):
            print(gap, results)
            print("common: {}".format(seq_results["common"]))
            print("diff_one: {}".format(seq_results["diff_one"]))
            print("diff_two: {}".format(seq_results["diff_two"]))
            print("\n")


if __name__ == "__main__":
    main()
    # seq_res = get_seq_types(['157', '491'])

    # for k, v in seq_res.items():
    #     print(k, v)
