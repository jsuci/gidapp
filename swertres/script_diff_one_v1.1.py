import fileinput
from itertools import product, islice
from re import split


def date_gap():
    """
    INPUT:
        prev_date - a string date (ex. 01 Wed May 2019 1) taken from
        results_count_missing_v1.1.txt

        curr_date - a string date (ex. 12 fri jul 2019 1) taken from
        results_v2.txt (results_v2.txt is used for more accurate date_gap
        count)

    OUTPUT:
        output - a list of tuple (ex. [(01 Wed May 2019, 1), (01 Wed May
        2019, 2), ...]) containing the date and int time
    """

    output = []
    found = False

    with open("results_diff_one_v1.1.txt", "r") as f1, \
            open("results_v2.txt", "r") as f2:

        prev_date = f1.readline().strip().replace("updated: ", "")
        curr_date = f2.readline().strip().replace("updated: ", "")
        p_date, p_int = [prev_date[:-2], int(prev_date[-1:])]

        for entry in islice(f2, 1, None):
            date_res = split(r"\s{2,}", entry.strip())
            c_date = date_res[0]
            len_results = len(date_res[1:])

            if prev_date == curr_date:
                break

            if p_date == c_date:
                found = True

            if found:
                for i in range(p_int, len_results):
                    output.append((c_date, i))
                    p_int = i

                    if p_int == 2:
                        p_int = 0

    return output[1:]


def get_time_results(prev_date):
    """
    INPUT:
        prev_date - a tuple (ex. '10 wed jul 2019', 1) taken from date_gap()

    OUTPUT:
        output - a list of results (ex. ['123', '456', ...])
    """

    output = []
    p_date = prev_date[0]
    p_int = prev_date[1]

    with open("results_v2.txt", "r") as fi:

        for entry in islice(fi, 2, None):
            entry = split(r"\s{2,}", entry.strip())
            results = entry[1:]
            date = entry[0]

            if p_date == date:
                for res in results[0:p_int + 1]:
                    output.insert(0, res)

                break

            else:
                for res in results:
                    output.insert(0, res)

    return output


def get_gap_results(all_results):
    """
    INPUT:
        all_results - a list of results (ex. ['473', '328'...005]) taken
        from get_time_results(prev_date)

    OUTPUT:
        gap_results - a list of tuple of gap and gap_results (ex. [10,
        ['123', '456', '789'], ...]
    """

    gap_results = []

    # Control the amount of results here
    for gap in range(1, 100):
        step = gap
        temp_results = []

        for count, result in enumerate(all_results):
            if step == count and len(temp_results) != 3:
                temp_results.append(result)

                step += (gap + 1)

            if len(temp_results) == 3:
                break

        if len(temp_results) < 3:
            break
        else:
            gap_results.append((gap, temp_results))

    return gap_results


def seq_type(digits):
    """
    Given a sequence of string numbers['8', '9', '0', '1'...] determine
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
    """Given a list of sequence['1', '2', '4'] and string
    of seq_type("diff_one", "diff_two" etc.) return a list
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
    """
    INPUT:
        results - a list of gap_results (ex. ["651", "226", "824"])

    OUTPUT:
        (all_sep_res, all_pairs, all_combi) - a tuple containing all
        results, pairs and combinations
    """

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
        if common and seq_type(seq) == "diff_one":
            # results = ['45', '56', '67']
            # common = 3
            # seq = ('4', '5', '6')

            # all_pairs = ['33', '37', '34', '38']
            pf_digits = possible_digits(seq, "diff_one")
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
            if seq_type(rm_results) == "diff_zero":
                pe_digits = possible_digits(rm_results, seq_type(rm_results))
                for combi in product(pairs, pe_digits):
                    all_combi.append("".join(combi))

            break

    if all_combi:
        return (all_sep_res, all_pairs, all_combi)
    else:
        return None


def find_diff_one():

    result_gap = date_gap()

    with open("results_diff_one_v1.1.txt", "a") as fo, \
            open("my_probables_v1.1.txt", "a") as fp:

        for prev_date in date_gap():

            print(f"date: {prev_date[0]} {prev_date[1]}")
            fo.write(f"date: {prev_date[0]} {prev_date[1]}\n")
            fp.write(f"date: {prev_date[0]} {prev_date[1]}\n")

            all_results = get_time_results(prev_date)

            for gap_results in get_gap_results(all_results):
                gap, results = gap_results

                if results and classify_results(results) is not None:
                    results, pairs, all_combi = classify_results(results)

                    # print("time: {}".format(time))
                    print("gap: {}".format(gap))
                    print("pairs: {}".format(pairs))
                    print("results:")

                    # fp.write("time: {}\n".format(time))
                    fo.write("gap: {}\n".format(gap))
                    fp.write("gap: {}\n".format(gap))
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

    if result_gap:
        with fileinput.input("results_diff_one_v1.1.txt", inplace=True) as fio:
            for entry in fio:
                if "updated:" in entry:
                    print(f"updated: {result_gap[-1][0]} {result_gap[-1][1]}")
                else:
                    print(entry, end="")


def main():
    find_diff_one()


if __name__ == "__main__":
    main()
