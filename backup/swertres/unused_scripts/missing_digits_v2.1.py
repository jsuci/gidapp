import re
from itertools import islice


def get_gap_results():
    """Gathers all gap results and returns a list of tuple
    containing the gap_value and time, results dictionary
    ex. [(2, {'11am': ['952', '517', '591'], '4pm': ['371',
    '976', '433'], '9pm': ['019', '928', '653']})...]
    """

    gap_results_list = []

    for gap_value in range(2, 20):
        with open("results_v2.txt", "r") as fo:
            last_entry = fo.readline().strip().split(" ")[-1]
            reversed_entries = list(islice(fo, 1, None))[::-1]
            to_skip = 0 if last_entry == "2" else 1
            step_value = gap_value + to_skip
            number_of_matches = 0
            gap_results = {"11am": [], "4pm": [], "9pm": []}

            for line_count, line_entry in enumerate(reversed_entries):
                date_results_list = re.split(r"\s{2,}", line_entry.strip())

                # Set number of matches here
                if line_count == step_value and number_of_matches != 2:
                    gap_results["11am"].append(date_results_list[1])
                    gap_results["4pm"].append(date_results_list[2])
                    gap_results["9pm"].append(date_results_list[3])

                    number_of_matches += 1
                    step_value += gap_value + 1

            gap_results_list.append((gap_value, gap_results))

    return gap_results_list


def is_sequence(list_of_digits):
    """Given a list of unsorted integers ex. [4, 8, 3, ...] from
    0 to 9 of any given length, check if all the values fit the
    conditions below:
        if all digits has a difference of 1 then return 1
        if some digits are in sequence and the other digit has
        a difference of of 2 then return 2
        else return 0
    """
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


def is_missing(results):
    """Given a list of results ex. ['358', '468', '827', ...]
    check if is in sync or not. By sync means it has:
        a. common_digit
        b. left and right digits must are in sequence

    If all conditions are satisfied then output  the following:
        a. left and right digits
        b. pair_common_digit
        c. common_digit

    ex. [3, 4, 2] [5, 6, 7] [('38', '58'), ('48', '68'),
    ('28', '78')] 8
    """
    for i in range(10):
        common_digit = str(i)
        has_common_digit = True
        left_digit = []
        right_digit = []
        pair_common_digit = []

        for result in results:
            if common_digit not in result:
                has_common_digit = False
            else:
                pairs = result.replace(common_digit, "", 1)
                left_pair = "".join([pairs[0], common_digit])
                right_pair = "".join([pairs[1], common_digit])

                left_digit.append(int(pairs[0]))
                right_digit.append(int(pairs[1]))
                pair_common_digit.append((left_pair, right_pair))

        if has_common_digit:
            """After you have identified results that has common
            digits you can now further filter the results by choosing
            wether the left or right digits is in sequence or has a
            gap of 2

            debug: print(left_digit, right_digit, left_seq, right_seq)
            """

            left_seq = is_sequence(left_digit)
            right_seq = is_sequence(right_digit)

            if (
                (left_seq == 1 or right_seq == 1) and
                (left_seq == 2 or right_seq == 2)
            ):
                return (left_digit, right_digit, pair_common_digit,
                        common_digit)


def main():
    for item in get_gap_results():
        gap_value, gap_results = item
        for time, results in gap_results.items():

            if is_missing(results):
                left, right, pairs, common = is_missing(results)

                print("gap: {}\ntime: {}\nresults: {}\n".format(
                    gap_value, time, results), end="")
                print("common_digit: {}\nleft: {}\n".format(
                    common, left), end="")
                print("right: {}\npairs (curr -> prev):".format(
                    right))

                for pair in pairs:
                    print(pair)

                print("\n\n")


if __name__ == "__main__":
    main()
