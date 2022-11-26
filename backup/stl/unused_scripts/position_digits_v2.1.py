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
                if line_count == step_value and number_of_matches != 5:
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


def is_position(results):
    """Given a list of results ex. ['358', '468', '827']
    (curr -> prev) check if is in sync or not. If yes
    then output left, right digits, pair_common_digit,
    common_digit ex. [3, 4, 2] [5, 6, 7] [('38', '58'),
    ('48', '68'), ('28', '78')] 8
    """
    first_pos = []
    second_pos = []
    third_pos = []

    for result in results:
        first_pos.append(int(result[0]))
        second_pos.append(int(result[1]))
        third_pos.append(int(result[2]))

    first_seq = is_sequence(first_pos)
    second_seq = is_sequence(second_pos)
    third_seq = is_sequence(third_pos)

    if first_seq == 1:
        first_pos_format = ["({}) {} {}".format(
            x[0], x[1], x[2]) for x in results]
        return (first_pos_format, 1)

    elif second_seq == 1:
        second_post_format = ["{} ({}) {}".format(
            x[0], x[1], x[2]) for x in results]
        return (second_post_format, 2)

    elif third_seq == 1:
        third_post_format = ["{} {} ({})".format(
            x[0], x[1], x[2]) for x in results]
        return (third_post_format, 3)
    else:
        return False


def main():
    for item in get_gap_results():
        gap_value, gap_results = item
        for time, results in gap_results.items():
            if is_position(results):
                exact_digits, position = is_position(results)

                print("gap: {}\ntime: {}\nresults: {}\n".format(
                    gap_value, time, results), end="")
                print("position: {}\n".format(
                    position), end="")
                print("exact (curr -> prev):")

                for digit in exact_digits:
                    print(digit)

                print("\n\n")


if __name__ == "__main__":
    main()
