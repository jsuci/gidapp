import re
from itertools import islice, combinations

def get_gap_results(gap_value):
    with open("results_v2.txt", "r") as fo:
        last_entry = fo.readline().strip().split(" ")[-1]
        reversed_entries = list(islice(fo, 1, None))[::-1]
        to_skip = 0 if last_entry != "2" else 1
        step_value = gap_value + to_skip
        number_of_matches = 0
        gap_results = {"11am": [], "4pm": [], "9pm": []}


        for line_count, line_entry in enumerate(reversed_entries):
            date_results_list = re.split(r"\s{10}", line_entry.strip())

            if line_count == step_value and number_of_matches != 4:
                gap_results["11am"].append(date_results_list[1])
                gap_results["4pm"].append(date_results_list[2])
                gap_results["9pm"].append(date_results_list[3])

                number_of_matches += 1
                step_value += gap_value + 1

        return gap_results

def is_sequence(results):
    check_first_digits = True

    start_digit = int(results[0][1])
    for result in islice(results, 1, None):
        next_digit = int(result[1])

        if abs(start_digit - next_digit) != 1:
            check_first_digits = False

        start_digit = next_digit

    return check_first_digits


def filter_gap_results(gap_results):
    for time, results in gap_results.items():
       if is_sequence(results):
        return time, results


def main():
    for gap_value in range(2, 20):
        gap_results = get_gap_results(gap_value)

        if filter_gap_results(gap_results):
            time, results = filter_gap_results(gap_results)
            print(gap_value, time, results)


if __name__ == "__main__":
    main()