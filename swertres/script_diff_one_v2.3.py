import fileinput
from datetime import datetime, timedelta
from itertools import product, islice
from pprint import pprint
from re import split


def date_gap():
    """Extract the date and time from results_v2.txt and
    results_diff_one_v2.2.txt and return a date-time object"""

    with open("results_diff_one_v2.3.txt", "r") as f1:
        prev_dt = f1.readline().strip().replace("updated: ", "")

    with open("results_v2.txt", "r") as f2:
        curr_dt = f2.readline().strip().replace("updated: ", "")

    prev_date = prev_dt
    curr_date, curr_int = [curr_dt[:-2], int(curr_dt[-1:])]

    prev_date = datetime.strptime(prev_date, "%d %a %b %Y")
    curr_date = datetime.strptime(curr_date, "%d %a %b %Y")

    if curr_int != 2:
        curr_date -= timedelta(days=1)

    return [prev_date, curr_date]


def result_gap():
    """Given two date-time objects calculate the difference
    in terms of days. Return an integer"""

    prev_dt, curr_dt = date_gap()
    time_diff = curr_dt - prev_dt

    return time_diff.days


def get_reverse_results(index=0):
    """Given all the results from results_v2.txt
    return a dictionary containing time results
    in this format

    {"11am": ['123', ...], "4pm": ['456', ...]..}
    """

    reverse = []
    time_results = {}

    with open("results_v2.txt", "r") as fi:
        for entry in islice(fi, 2, None):
            entry = entry.strip()
            reverse.insert(0, entry)

    for r_entry in reverse[index:]:
        results = split(r"\s{2,}", r_entry)[1:]
        if len(results) == 3:
            time_results.setdefault("11am", [])
            time_results.setdefault("4pm", [])
            time_results.setdefault("9pm", [])

            time_results["11am"].append(results[0])
            time_results["4pm"].append(results[1])
            time_results["9pm"].append(results[2])

    return time_results


def get_gap_results(time_results):

    gap_results = {}

    for time, results in time_results.items():

        # Control the amount of results here
        for gap in range(1, 50):
            step = gap
            temp_results = []

            for count, result in enumerate(results):
                if step == count and len(temp_results) != 3:
                    temp_results.append(result)

                    step += (gap + 1)

            gap_results.setdefault(time, {})
            gap_results[time].setdefault(gap, temp_results)

    return gap_results


"""The functions below are responsible for
processing get_gap_results"""


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
            diff_one_count == 1 and
            diff_two_count == 1 and
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


def possible_digits(sequence, seq_type):
    """Given a list of sequence ['1', '2', '4'] and string
    of seq_type ("diff_one", "diff_two" etc.) return a list
    of possible digit(s).
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

    def diff_zero_next(sequence):
        return str(next(iter(set(sequence))))

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

    def has_double_next(sequence):

        for digit in set(sequence):
            if sequence.count(digit) != 2:
                return str(digit)

    if seq_type == "diff_one":
        output = diff_one_next(sequence)

    elif (
        seq_type == "diff_two" or
        seq_type == "gap_one"
    ):
        output = diff_two_next(sequence)

    elif seq_type == "has_double":
        output = has_double_next(sequence)

    elif seq_type == "diff_zero":
        output = diff_zero_next(sequence)

    else:
        output = "invalid seq_type"

    return output


def classify_results(results):
    """Given a list of results determine if all the result contains
    a common_digit and has diff_one pattern"""

    common = ""
    all_sep_res = []
    all_pairs = []
    all_combi = []

    # Process the first element of results
    for digit in results[0]:
        if digit in results[1] and digit in results[2]:
            common = digit
            results = [results[i].replace(digit, "", 1)
                       for i in range(len(results))]
            break

    # Process the second element of results
    for seq in product(*results):
        if seq_type(seq) == "diff_one" and common:
            # results = ['45', '56', '67']
            # common = 3
            # seq = ('4', '5', '6')

            # all_pairs = ['33', '37', '34', '38']
            pf_digits = possible_digits(seq, "diff_one")
            pairs = [x + y for x, y in product(common, pf_digits)]
            all_pairs.extend(pairs)

            # all_sep_res = ['34-5', '35-6', ...]
            rm_results = list(map(lambda x: x[1].replace(seq[x[0]], "", 1),
                                  enumerate(results)))
            sep_results = list(map(lambda x: "{}{}-{}".format(
                               common, seq[x[0]], x[1]), enumerate(rm_results)))
            all_sep_res.extend(sep_results)

            # all_combi
            if seq_type(rm_results) != None:
                # pe_digits = [n] or pe_digits = [n, n + 1]
                pe_digits = possible_digits(rm_results, seq_type(rm_results))
                for combi in product(pairs, pe_digits):
                    all_combi.append("".join(combi))

            break

    if all_combi:
        return (all_sep_res, all_pairs, all_combi)
    else:
        return None


def find_diff_one():

    with open("results_diff_one_v2.3.txt", "a") as fo, \
            open("my_probables_v2.3.txt", "a") as fp:

        prev_date, curr_date = date_gap()

        for i in reversed(range(result_gap())):
            prev_date += timedelta(days=1)

            print("date: {}".format(
                prev_date.strftime("%d %a %b %Y")))

            fo.write("date: {}\n".format(
                prev_date.strftime("%d %a %b %Y")))
            fp.write("date: {}\n".format(
                prev_date.strftime("%d %a %b %Y")))

            time_results = get_reverse_results(i)

            for time, gap_results in get_gap_results(time_results).items():
                for gap, results in gap_results.items():

                    if classify_results(results):
                        results, pairs, all_combi = classify_results(results)

                        print("time: {}".format(time))
                        print("gap: {}".format(gap))
                        print("pairs: {}".format(pairs))
                        print("results:")

                        fo.write("time: {}\n".format(time))
                        fp.write("time: {}\n".format(time))
                        fo.write("gap: {}\n".format(gap))
                        fo.write("pairs: {}\n".format(pairs))
                        fo.write("results:\n")

                        for res in results:
                            print(res)
                            fo.write("{}\n".format(res))

                        for probables in all_combi:
                            fp.write("{}\n".format(probables))

                        print("\n")

                        fp.write("\n")
                        fo.write("\n")

            print("\n")

            fo.write("\n\n")
            fp.write("\n\n")

    with fileinput.input("results_diff_one_v2.3.txt", inplace=True) as fio:
        for entry in fio:
            if "updated:" in entry:
                print("updated: {}".format(
                    curr_date.strftime("%d %a %b %Y")))
            else:
                print(entry, end="")


def main():
    find_diff_one()


if __name__ == "__main__":
    main()
