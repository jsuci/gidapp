from itertools import *
from re import *
import fileinput

"""
Using this script filter results that contains common_digit
only ex: ['666', '456', '673']

Output:
    gap: 18
    common: 6
    results: ['666', '456', '673']
    seq_types:
    ('6', '4', '7') <- gap_one
    ('6', '4', '3') <- gap_one
    ('6', '5', '7') <- diff_one
    ('6', '5', '3') <- gap_one

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
        output_item = (list(seq), seq_type(seq))

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

            if common_list and len(common_list) >= 2:
                seq_types = get_seq_types(common_list, common)
                final_list.append((
                    gap_value, common, common_list, seq_types))

    return final_list


def export_file(gap, common, results, seq_types, pairs):

    with open("results_diff_zero_v1.3.txt", "a") as fo:
        fo.write("pair: {}\n".format(pairs))
        fo.write("results: {}\n".format(results))
        fo.write("\n")
        # fo.write("common: {}\n".format(common))
        # fo.write("seq_types:\n")
        # for seq in seq_types:
        #     fo.write("{} <- {}\n".format(seq[0], seq[1]))


def check_date():
    """Check results_v1.txt current date and compare it to the
    results_diff_zero date. Return True if they are the same and
    False if not"""

    with open("results_v1.txt", "r") as fi:
        with open("results_diff_zero_v1.3.txt", "r") as fo:
            fi_date = fi.readline().strip()
            fo_date = fo.readline().strip()

            if fi_date != fo_date:
                return fi_date


def get_current_date():
    """Get current date"""

    with open("results_v1.txt") as fi:
        first_line = fi.readline().strip()
        return findall(r"(?<=updated: )(\S.+)", first_line)[0]


def main():

    if not check_date():
        print("Results are up to date.")
    else:
        with open("results_diff_zero_v1.3.txt", "a") as fo:
            date = get_current_date()
            fo.write("\nDATE GENERATED: {}\n".format(date))

        for entry in filter_results():
            gap, common, results, seq_types = entry

            if (
                len(seq_types) == 2 and
                "diff_zero" in chain(*seq_types)
            ):
                pairs = ""

                print("gap: {}".format(gap))
                print("common: {}".format(common))
                print("results: {}".format(results))
                print("pairs: {}".format(pairs))
                print("seq_types:")
                for seq in seq_types:
                    if seq[1] == "diff_zero":
                        pairs = common + seq[0][0]
                    print("{} <- {}".format(seq[0], seq[1]))
                print("\n")

                export_file(gap, common, results, seq_types, pairs)

                with fileinput.input("results_diff_zero_v1.3.txt",
                                     inplace=True) as fio:
                    for entry in fio:
                        if "updated:" in entry:
                            print(check_date())
                        else:
                            print(entry, end="")


if __name__ == "__main__":
    main()
