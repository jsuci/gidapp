from itertools import *

"""
Using this script filter results that contains common_digit and
first result and the third result has two common_digits
ex: ['928', '965', '729']. From the example 92 appears on the
first and third result

Output:
    gap: 130
    common: 9
    results: ['928', '965', '729']
    seq_types:
    ('2', '6', '2') <- has_double
    ('2', '5', '2') <- has_double
    ('8', '6', '7') <- diff_one
    ('8', '5', '7') <- gap_one

The purpose of this script is to observe common patterns between gap
of common digits on results_v1.txt
"""


def get_results():
    """Get all the previous result and store it in reverse order"""

    results = []
    with open("results_v1.txt", "r") as fi:
        for line in islice(fi, 2, None):
            results.insert(0, line.strip())

    return results


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

    for seq in product(*trim_results):
        output_item = (seq, seq_type(seq))
        if seq_type(seq) and output_item not in output:
            output.append(output_item)

    return output


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


def export_file(gap, common, results, gen_pairs, combi):

    with open("results_common_pairs_v1.1.txt", "a") as fo:
        fo.write("gap: {}\n".format(gap))
        fo.write("common: {}\n".format(common))
        fo.write("results: {}\n".format(results))
        fo.write("next_pairs: {}\n".format(gen_pairs))
        fo.write("possible_combi:\n")
        for p_combi in combi:
            fo.write("{}\n".format(p_combi))
        fo.write("\n\n")


def compare_digits(digit_1, digit_2):

    for num_1 in digit_1:
        if num_1 in digit_2:
            digit_2 = digit_2.replace(num_1, "", 1)

    # Check if digits has two common digits
    if len(digit_2) <= 1:
        return True
    else:
        return False


def gen_pairs(digit):
    return ", ".join(["".join(e) for e in combinations(digit, 2)])


def plus_one(digit):
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


def minus_one(digit):
    return {
        1: 0,
        2: 1,
        3: 2,
        4: 3,
        5: 4,
        6: 5,
        7: 6,
        8: 7,
        9: 8,
        0: 9
    }[digit]


def possible_combi(digit, common):
    """Given a digit and its common number, generate possible
    combinations by adding and subtracting each or all digit
    by 1
    ex:
        pair: 92
        plus_all: 03
        minus_all: 81
        plus_minus: 83
        minus_plus: 03
    """

    pair = [int(e) for e in digit.replace(common, "", 1)]

    plus_all = [str(plus_one(e)) for e in pair]
    minus_all = [str(minus_one(e)) for e in pair]

    plus_minus = [str(plus_one(pair[0])), str(minus_one(pair[1]))]
    minus_plus = [str(minus_one(pair[0])), str(plus_one(pair[1]))]

    plus_left = [str(plus_one(pair[0])), str(pair[1])]
    plus_right = [str(pair[0]), str(plus_one(pair[1]))]

    minus_left = [str(minus_one(pair[0])), str(pair[1])]
    minus_right = [str(pair[0]), str(minus_one(pair[1]))]

    combined = ["".join(e) for e in (
        plus_all, minus_all, plus_minus, minus_plus,
        plus_left, plus_right, minus_left, minus_right)]

    final_result = []

    for seq in product(combined, common):
        combi = seq[0] + seq[1]

        final_result.append(combi)

    return final_result


def main():
    with open("results_common_pairs_v1.1.txt", "w") as fi:
        fi.write("")

    for entry in filter_results():
        gap, common, results, seq_types = entry
        combi = possible_combi(results[1], common)
        pairs = gen_pairs(results[1])

        if compare_digits(results[0], results[2]):
            print("gap: {}".format(gap))
            print("common: {}".format(common))
            print("results: {}".format(results))
            print("next_pairs: {}".format(pairs))
            print("possible_combi:")
            for p_combi in combi:
                print(p_combi)


            export_file(gap, common, results, pairs, combi)
            print("\n")


if __name__ == "__main__":
    main()
