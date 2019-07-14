from itertools import islice
from re import split
import fileinput


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

    with open("results_count_missing_v1.1.txt", "r") as f1, \
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

    return output


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


def count_missing_digit(all_results, digit):
    """
    INPUT:
        all_results - a list of results (ex. ['473', '328'...005]) taken
        from get_time_results(prev_date)

        digit - a string int (ex. "1")

    OUTPUT:
        final_result - a list composed of string digit and a dictionary
        (ex. ["0", {"first": 0, "second": 0, "third": 0}])
    """

    first_count = 0
    second_count = 0
    third_count = 0
    highest_count = 0
    highest_format = ""

    final_result = [digit, {"first": 0, "second": 0, "third": 0}]

    for result in all_results:
        if digit != result[0]:
            first_count += 1
        else:
            final_result[1]["first"] = first_count
            if highest_count < first_count:
                highest_count = first_count
                highest_format = "{} - -".format(digit)
            break

    for result in all_results:
        if digit != result[1]:
            second_count += 1
        else:
            final_result[1]["second"] = second_count
            if highest_count < second_count:
                highest_count = second_count
                highest_format = "- {} -".format(digit)
            break

    for result in all_results:
        if digit != result[2]:
            third_count += 1
        else:
            final_result[1]["third"] = third_count
            if highest_count < third_count:
                highest_count = third_count
                highest_format = "- - {}".format(digit)
            break

    final_result.extend([highest_count, highest_format])

    return final_result


def all_missing_digit():

    result_gap = date_gap()

    with open("results_count_missing_v1.1.txt", "a") as fo:

        for prev_date in result_gap:
            print(f"date: {prev_date[0]} {prev_date[1]}")
            fo.write(f"date: {prev_date[0]} {prev_date[1]}\n")

            time_results = get_time_results(prev_date)

            print(f"result: {time_results[0]}")
            fo.write(f"result: {time_results[0]}\n")

            all_missing = []

            for i in range(10):
                all_missing.append(count_missing_digit(
                    time_results, str(i)))

            sorted_missing = sorted(
                all_missing, key=(lambda x: x[2]), reverse=True)

            for entry in sorted_missing:
                print(f"{entry[0]} <- {entry[2]:2}\t\t{entry[3]}")
                fo.write(f"{entry[0]} <- {entry[2]:2}\t\t{entry[3]}\n")

            print("\n\n")
            fo.write("\n\n")

    if result_gap:
        with fileinput.input(
                "results_count_missing_v1.1.txt", inplace=True) as fio:
            for entry in fio:
                if "updated:" in entry:
                    print(f"updated: {result_gap[-1][0]} {result_gap[-1][1]}")
                else:
                    print(entry, end="")


def main():
    all_missing_digit()


if __name__ == "__main__":
    main()
