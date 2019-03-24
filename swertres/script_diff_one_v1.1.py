import fileinput
from itertools import *
from re import *
from pprint import *
from datetime import *


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


def get_gap_results_v1():

    def get_reverse_results_v1():
        """Given all the results from results_v2.txt
        return a list containing results in this
        reverse order.

        ['123', ...]
        """

        reverse = []

        with open("results_v1.txt", "r") as fi:
            for entry in islice(fi, 2, None):
                entry = entry.strip()
                reverse.insert(0, entry)

        return reverse

    results = get_reverse_results_v1()
    gap_results = {}

    for gap in range(1, 20):
        step = gap
        temp_results = []

        for count, result in enumerate(results):
            if step == count and len(temp_results) != 3:
                temp_results.append(result)
                step += (gap + 1)

            gap_results.setdefault(gap, temp_results)

    return gap_results


def get_pos_digits(sequence, seq_type):
    """Given a list of sequence ['1', '2', '4'] and string
    of seq_type ("diff_one", "diff_two" etc.) return a list
    of possible digit(s).

    ex.
        ['9', '0']
        ['1']
    """

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
            0: 9,
            9: 8,
            8: 7,
            7: 6,
            6: 5,
            5: 4,
            4: 3,
            3: 2,
            2: 1,
            1: 0
        }[digit]

    def diff_one_next(sequence):

        sort_entry = sorted([str(e) for e in sequence])

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

        return [str(start_digit), str(last_digit)]

    def diff_two_next(sequence):

        sort_entry = sorted([str(e) for e in sequence])

        if (
            '1' in sort_entry and
            '9' in sort_entry
        ):
            between_digit = plus_one('9')

        elif (
            '0' in sort_entry and
            '8' in sort_entry
        ):
            between_digit = plus_one('8')

        else:
            start = sort_entry[0]
            for digit in islice(sort_entry, 1, None):
                if int(digit) - int(start) == 2:
                    between_digit = plus_one(start)
                start = digit

        return [str(between_digit)]

    if seq_type == "diff_one":
        output = diff_one_next(sequence)
    elif (
        seq_type == "diff_two" or
        seq_type == "gap_one"
    ):
        output = diff_two_next(sequence)
    else:
        print("invalid seq_type.")

    return output


def get_generated_date_v1():
    """Get current date from updated string of
    results_v2.txt. Return a string of date
    """

    with open("results_v1.txt") as fi:
        date = fi.readline().strip().replace("updated: ", "")

    return date


def get_expected_date_v1():
    gen_date = get_generated_date_v1().split(" ")
    exp_date = (datetime.now().replace(day=int(gen_date[0])) +
                timedelta(days=0))

    day = exp_date.day
    weekday = exp_date.strftime("%a").lower()
    month = exp_date.strftime("%b").lower()
    year = exp_date.year

    return "{} {} {} {} {}".format(
        day, weekday, month, year, gen_date[-1])


def is_current_date():
    """Get results_v2.txt current date and compare it to
    results_seq_types_v2.1.txt date. Return True if they
    are the same and False if not
    """

    with open("results_diff_one_v1.1.txt", "r") as fo:
        fi_date = "updated: " + get_generated_date_v1()
        fo_date = fo.readline().strip()

        if fi_date != fo_date:
            return fi_date


def is_pure_diff_one(results, d_one_seq):
    filter_res = []
    for res_c, result in enumerate(results):
        for seq in d_one_seq:
            result = result.replace(seq[res_c], "", 1)
        filter_res.append(result)

    if len(set(filter_res)) == 1:
        return True
    else:
        return False


def export_results():
    """After getting the get_gap_results_v1 filter
    the results by its seq_type, common etc
    """

    with open("results_diff_one_v1.1.txt", "a") as fo:

        fo.write("DATE_GENERATED: {}\n".format(
            get_generated_date_v1()))
        fo.write("DATE_EXPECTED: {}\n".format(
            get_expected_date_v1()))
        fo.write("DRAWS: 1 - 2 draws\n")

        gap_results = get_gap_results_v1()
        pair_results = []

        for gap, results in gap_results.items():
            seq_types = get_seq_types(results)

            # Filter options currently set to:
            # common(2)
            if (
                "common" in seq_types and
                len(seq_types["common"]) == 1 and
                "diff_one" in seq_types and
                len(seq_types["diff_one"]) >= 1
            ):
                fo.write("gap: {}\n".format(gap))
                fo.write("common: {}\n".format(seq_types["common"]))
                fo.write("results:\n")
                for res in results:
                    fo.write("{}\n".format(res))

                fo.write("\n")

        fo.write("{}\n".format(", ".join(pair_results)))

    with fileinput.input("results_diff_one_v1.1.txt",
                         inplace=True) as fio:
        for entry in fio:
            if "updated:" in entry:
                print(is_current_date())
            else:
                print(entry, end="")


def filter_results():
    """After getting the get_gap_results_v1 filter
    the results by its seq_type, common etc
    """

    print("DATE_GENERATED: {}".format(
        get_generated_date_v1()))
    print("DATE_EXPECTED: {}".format(
        get_expected_date_v1()))
    print("DRAWS: 1 - 2 draws\n")

    gap_results = get_gap_results_v1()

    for gap, results in gap_results.items():
        seq_types = get_seq_types(results)

        # Filter options currently set to:
        # common(2)
        if (
            "common" in seq_types and
            len(seq_types["common"]) == 1 and
            "diff_one" in seq_types and
            len(seq_types["diff_one"]) >= 1
        ):

            print("gap: {}".format(gap))
            print("common: {}".format(seq_types["common"]))
            print("results:")
            for res in results:
                print(res)

            print("\n")


def main():
    filter_results()

    if not is_current_date():
        print("Results are up to date.")
    else:
        export_results()


if __name__ == "__main__":
    main()
