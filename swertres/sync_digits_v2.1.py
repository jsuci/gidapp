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
                date_results_list = re.split(r"\s{10}", line_entry.strip())

                # Set number of matches here
                if line_count == step_value and number_of_matches != 3:
                    gap_results["11am"].append(date_results_list[1])
                    gap_results["4pm"].append(date_results_list[2])
                    gap_results["9pm"].append(date_results_list[3])

                    number_of_matches += 1
                    step_value += gap_value + 1

            gap_results_list.append((gap_value, gap_results))

    return gap_results_list


def is_sequence(list_digits):
    """Given a list of unsorted integers ex. [4, 8, 3] check
    if all the values inside has a difference of one.
    """
    sorted_digits = sorted(list_digits)
    start = sorted_digits[0]
    result = True

    for digit in islice(sorted_digits, 1, None):

        """Catch case where in [0, 8, 9] and [0, 1, 9]
        are considered sequence. Note that digits are in
        length of 3
        """
        if not (
            (start == 0 and abs(start - digit) == 8) or
            (start == 1 and abs(start - digit) == 8) or
                (abs(start - digit) == 1)):

            result = False

        start = digit

    return result


def is_sync(results):
    """Given a list of results ex. ['358', '468', '827']
    check if is in sync or not. If yes then output left,
    right digits, pair_common_digit, common_digit
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
                left_digit.append(int(pairs[0]))
                right_digit.append(int(pairs[1]))
                pair_common_digit.append(("".join([pairs[0], common_digit]),
                                          "".join([pairs[1], common_digit])))

        if has_common_digit and is_sequence(
                left_digit) and is_sequence(right_digit):
            return left_digit, right_digit, pair_common_digit, common_digit


def main():
    for item in get_gap_results():
        gap_value, gap_results = item
        for time, results in gap_results.items():
            if is_sync(results):
                left, right, pairs, common = is_sync(results)

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
