from itertools import *
from re import *

"""
Using this script filter results that contains
two diff_one with maximum number of matches to 3

Output:
    gap: 40
    common: 5
    results: ['456', '375', '575']
    seq_types:
    ('4', '3', '5') <- diff_one
    ('4', '7', '7') <- has_double
    ('4', '7', '5') <- gap_one
    ('6', '3', '5') <- gap_one
    ('6', '7', '7') <- has_double
    ('6', '7', '5') <- diff_one


    gap: 443
    common: 5
    results: ['395', '527', '185']
    seq_types:
    ('3', '2', '1') <- diff_one
    ('9', '2', '1') <- gap_one
    ('9', '7', '1') <- diff_two
    ('9', '7', '8') <- diff_one

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

    for gap_value in range(1, 500):
        for common_digit in range(0, 10):
            common = str(common_digit)
            step = gap_value
            common_list = []

            for count, result in enumerate(results):
                if step == count and common in result:
                    common_list.append(result)
                    step += (gap_value + 1)

            if common_list and len(common_list) >= 3:

                # Limit to last 3 results only
                common_list = common_list[:3]

                seq_types = get_seq_types(common_list, common)
                final_list.append((
                    gap_value, common, common_list, seq_types))

    return final_list


def export_file(gap, common, results, seq_types, poss_combis):

    with open("results_diff_one_v1.1.txt", "a") as fo:
        fo.write("gap: {}\n".format(gap))
        fo.write("common: {}\n".format(common))
        fo.write("results: {}\n".format(results))
        fo.write("combi: {}\n".format(poss_combis))
        fo.write("seq:\n")
        for seq in seq_types:
            fo.write("{} <- {}\n".format(seq[0], seq[1]))
        fo.write("\n\n")


def compare_digits(digit_1, digit_2):

    for num_1 in digit_1:
        if num_1 in digit_2:
            digit_2 = digit_2.replace(num_1, "", 1)

    if len(digit_2) == 0:
        return True
    else:
        return False


def unique_diff_one(diff_one_list, pairs):

    for count, seq in enumerate(zip_longest(*diff_one_list)):

        if not compare_digits(seq, pairs[count]):
            return False

    return True


def plus_one(digit):
    digit = int(digit)

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
    digit = int(digit)

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


def possible_combi(diff_one_list, common):
    all_pairs = []
    combi = []

    for entry in diff_one_list:
        sort_entry = sorted(entry)

        if (
            '0' in sort_entry and
            '1' in sort_entry and
            '9' in sort_entry
        ):
            start_digit = minus_one('9')
            last_digit = plus_one('1')

        elif (
            '0' in sort_entry and
            '8' in sort_entry and
            '9' in sort_entry
        ):
            start_digit = minus_one('8')
            last_digit = plus_one('0')

        else:
            start_digit = minus_one(sort_entry[0])
            last_digit = plus_one(sort_entry[-1])

        pair = "".join([str(e) for e in (start_digit, last_digit)])
        all_pairs.append(pair)

    for seq in product(*all_pairs, common):
        combi.append("".join(seq))

    return combi


def get_current_date():
    """Get current date"""

    with open("results_v1.txt") as fi:
        first_line = fi.readline().strip()

        return findall(r"(?<=updated: )(\S.+)", first_line)[0]


def main():
    with open("results_diff_one_v1.1.txt", "w") as fo:
        date = get_current_date()
        fo.write("DATE GENERATED: {}\n".format(date))

    for entry in filter_results():
        gap, common, results, seq_types = entry
        pairs = [e.replace(common, "", 1) for e in results]
        diff_one_list = [e[0] for e in seq_types if e[1] == "diff_one"]

        if (
            len(diff_one_list) == 2 and
            unique_diff_one(diff_one_list, pairs)
        ):

            poss_combis = possible_combi(diff_one_list, common)

            print("gap: {}".format(gap))
            print("common: {}".format(common))
            print("results: {}".format(results))
            print("combi: {}".format(poss_combis))
            print("seq:")
            for seq in seq_types:
                print("{} <- {}".format(seq[0], seq[1]))
            print("\n\n")

            export_file(gap, common, results, seq_types, poss_combis)


if __name__ == "__main__":
    main()
