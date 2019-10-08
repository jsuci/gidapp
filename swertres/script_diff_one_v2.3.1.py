import fileinput
from itertools import product, islice
from re import split


def date_gap():
    """
    INPUT:
    results_diff_one_v2.3.txt - get the previous date
    results_v2.txt - get the current date

    OUTPUT:
    output - a list containing dates from prev_dt to
    curr_dt
    ex.
        ["02 tue jan 2018"..."22 sat jun 2019"]
    """

    output = []
    found = False

    with open("results_diff_one_v2.3.1.txt", "r") as f1, \
            open("results_v2.txt", "r") as f2:

        prev_date = f1.readline().strip().replace("updated: ", "", 1)

        for entry in islice(f2, 1, None):
            entry = entry.strip()
            date = split(r"\s{2,}", entry)

            if prev_date == date[0]:
                found = True
                continue

            if len(date) == 4 and (found or len(output) >= 1):
                output.append(date[0])

    return output


def get_time_results(prev_date):
    """
    INPUT:
    prev_date - a string taken from date_gap()
    ex.
        ("02 tue jan 2018")

    OUTPUT:
    time_results - a dictionary of time and results
    ex.
        {"11am": ['123', ...], "4pm": ['456', ...]..}
    """

    time_results = {}

    with open("results_v2.txt", "r") as fi:

        for entry in islice(fi, 2, None):
            entry = entry.strip()
            results = split(r"\s{2,}", entry)
            date = results[0]

            if prev_date == date and len(results) == 4:
                time_results.setdefault("11am", [])
                time_results.setdefault("4pm", [])
                time_results.setdefault("9pm", [])

                time_results["11am"].append(results[1])
                time_results["4pm"].append(results[2])
                time_results["9pm"].append(results[3])

                break

            elif prev_date != date and len(results) == 4:
                time_results.setdefault("11am", [])
                time_results.setdefault("4pm", [])
                time_results.setdefault("9pm", [])

                time_results["11am"].append(results[1])
                time_results["4pm"].append(results[2])
                time_results["9pm"].append(results[3])

            else:
                pass

    return time_results


def get_gap_results(time_results):

    gap_results = {}

    for time, results in time_results.items():

        # Control the amount of results here
        for gap in range(1, 50):
            step = gap
            temp_results = []

            for count, result in enumerate(reversed(results)):
                if step == count and len(temp_results) != 3:
                    temp_results.append(result)

                    step += (gap + 1)

                if len(temp_results) == 2:
                    break

            if len(temp_results) < 2:
                break
            else:
                gap_results.setdefault(time, {})
                gap_results[time].setdefault(gap, temp_results)

    # print(gap_results)
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
            diff_two_count == 1 and diff_none_count != 2
        ):
            return "diff_two"

        # Filter error_seq
        if diff_none_count >= 2:
            return "error_seq"

        # Filter gap_one
        # if (
        #     diff_one_count != 0 and
        #     diff_two_count == 1 and
        #     diff_none_count != 2
        # ):
        #     return "gap_one"


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

        # Filter and fix 0 and 9 output for diff_one
        # Hard coded length of values change as needed
        if (
            '0' in sort_entry and '1' in sort_entry
        ):
            start_digit = minus_one('0')
            last_digit = plus_one('1')

        elif (
            '0' in sort_entry and '9' in sort_entry
        ):
            start_digit = minus_one('9')
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
        output = []

    return output


def classify_results(results):
    """
    INPUT:
    results - a list of gap_results
    ex.
        ["651", "226", "824"]

    OUTPUT:
    (all_sep_res, all_pairs, all_combi) - a tuple containing
    all the results, pairs and combinations
    """

    common = ""
    all_sep_res = []
    all_pairs = []
    all_combi = []

    # Compare the first digit of the first result to the next digit
    # of the next result
    for digit in results[0]:
        if digit in results[1]:
            common = digit
            results = [results[i].replace(digit, "", 1)
                       for i in range(len(results))]
            break

    # Process the second element of results
    for seq in product(*results):
        if common and seq_type(seq) != "error_seq":
            # results = ['45', '56', '67']
            # common = 3
            # seq = ('4', '5', '6')

            # all_pairs = ['33', '37', '34', '38']
            pf_digits = possible_digits(seq, seq_type(seq))
            pairs = [x + y for x, y in product(common, pf_digits)]
            all_pairs.extend(pairs)

            # all_sep_res = ['34-5', '35-6', ...]
            rm_results = list(map(lambda x: x[1].replace(
                seq[x[0]], "", 1), enumerate(results)))

            sep_results = list(map(lambda x: "{}{}-{}".format(
                common, seq[x[0]], x[1]), enumerate(rm_results)))

            all_sep_res.extend(sep_results)

            # Filter the remaining digits by seq_type() here
            # all_combi = ['442', '482']
            if seq_type(rm_results) is not None:
                pe_digits = possible_digits(rm_results, seq_type(rm_results))
                for combi in product(pairs, pe_digits):
                    all_combi.append("".join(combi))

            break

    if all_combi:
        return (all_sep_res, all_pairs, all_combi)
    else:
        return None


def find_diff_one():

    with open("results_diff_one_v2.3.1.txt", "a") as fo, \
            open("my_probables_v2.3.1.txt", "a") as fp:

        for prev_date in date_gap():

            print("date: {}".format(prev_date))
            fo.write("date: {}\n".format(prev_date))
            fp.write("date: {}\n".format(prev_date))

            time_results = get_time_results(prev_date)

            for time, gap_results in get_gap_results(time_results).items():
                for gap, results in gap_results.items():

                    if results and classify_results(results) is not None:
                        results, pairs, all_combi = classify_results(results)

                        print("time: {}".format(time))
                        print("gap: {}".format(gap))
                        print("pairs: {}".format(pairs))
                        print(f"combis: {all_combi}")
                        print("results:")

                        # fp.write("gap: {}\n".format(gap))
                        # fp.write("time: {}\n".format(time))

                        fo.write("time: {}\n".format(time))
                        fo.write("gap: {}\n".format(gap))
                        fo.write("pairs: {}\n".format(pairs))
                        fo.write(f"combis: {all_combi}\n")
                        fo.write("results:\n")

                        for res in reversed(results):
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

    if date_gap():
        with fileinput.input("results_diff_one_v2.3.1.txt", inplace=True) as fio:
            for entry in fio:
                if "updated:" in entry:
                    print("updated: {}".format(date_gap()[-1]))
                else:
                    print(entry, end="")


def main():
    find_diff_one()
    # print(classify_results(["894", "852"]))


if __name__ == "__main__":
    main()
