"""
01 thu mar 2018 (7 steps skip)
353 <- 35
...
577 <- 77
...
053 <- 35
...
665 <- 66 (665 confirmed!)

On 01 thu mar 2018 a pattern was formed base on the common digit of 5.
Every 7 steps there is a 5 and these results that has common digit in
them form an alternating pattern.

What this script will do is:
1. search through all the list of results
2. filter only results that has a common digit and length of 3
3. after filtering check the pairs of each result. check if:
    a. first(prev), second(prev), third(curr) pairs are in sequence
    ex.
        [(20), 90]
        [(30), 80]
        [(40), 80]

    b. first and second pairs are the same
    ex.
        [20, 90]
        [30, (80)]
        [40, (80)]

    c. first and third pairs are the same
    ex.
        [05, (35)]
        [75, 77]
        [33, (35)]

"""

from itertools import *


def get_results():
    """Get all the previous result and store it in reverse order"""

    results = []
    with open("results_v1.txt", "r") as fi:
        for line in islice(fi, 2, None):
            results.insert(0, line.strip())

    return results


def get_pairs(digit):
    """Given any digit return pairs of that digit"""
    result = []

    for pair in combinations(digit, 2):
        pair = "".join(pair)
        result.append(pair)

    return result


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


def get_seq_types(results, common):
    pairs = [e.replace(common, "", 1) for e in results]
    seq_type_list = []

    for seq in product(*pairs):
        # common_seq = [e + common for e in seq]

        if (
            seq_type(seq) and
            (seq, seq_type(seq)) not in seq_type_list
        ):
            seq_type_list.append((seq, seq_type(seq)))

    return seq_type_list


def filter_results():
    """Process get_results() output and filter them by gap.
    Return a list of tuple containing [(gap_value, common, results)]
    """

    results = get_results()
    final_list = []

    for gap_value in range(1, 100):
        for common_digit in range(0, 10):
            common = str(common_digit)
            step = gap_value
            common_list = []

            for count, result in enumerate(results):
                if step == count and common in result:
                    common_list.append(result)
                    step += (gap_value + 1)

            if common_list and len(common_list) >= 3:
                seq_types = get_seq_types(common_list, common)
                final_list.append((
                    gap_value, common, common_list, seq_types))

    return final_list


def main():
    for entry in filter_results():
        gap, common, results, seq_types = entry
        print("gap: {}".format(gap))
        print("common: {}".format(common))
        print("results: {}".format(results))
        print("seq_types:")
        for seq in seq_types:
            sequence, label = seq
            print("{} <- {}".format(sequence, label))
        print("\n")


if __name__ == "__main__":
    main()
