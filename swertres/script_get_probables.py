from itertools import islice, product
from pathlib import Path
from re import split


def get_all_results():
    file_name = Path("results_v2.txt")
    key_names = ["11am", "4pm", "9pm"]
    date_results = []
    output = []

    with open(file_name, "r") as fi:
        for entry in islice(fi, 2, None):
            date_results.insert(0, split(r"\s{2,}", entry.strip()))

    for common_digit in range(0, 10):
        common_digit = str(common_digit)

        # {"11am": [("123", [], 6, "12 sat oct 2019")...]}
        time_results = {}

        # ["12 sat oct 2019", "123", "456", "789"]
        for entry in date_results:
            # "12 sat oct 2019"
            date = entry[0]

            # ["123", "456", "789"]
            for count, item in enumerate(entry[1:]):
                # 10
                sum_result = sum([int(x) for x in item])
                if common_digit in item:
                    # 12
                    remove_common = item.replace(common_digit, "", 1)
                    # ["01", "02"]
                    pairs = sorted(map(lambda x: "".join(x), product(
                        common_digit, remove_common)))

                    time_results.setdefault(key_names[count], [])
                    time_results[key_names[count]].append(
                        (item, pairs, sum_result, date))
                else:

                    time_results.setdefault(key_names[count], [])
                    time_results[key_names[count]].append(
                        (item, [], sum_result, date))

        output.append((common_digit, time_results))

    # [("0",
    #   {
    #   "11am": [("123", [21, 23], 6)...],
    #   "4am": [("456", [45, 46], 15)...],
    #   "9pm": [("789", [], 24)...]}),..]
    #   }
    # )]
    return output


def get_gap_results():

    def make_gaps(results):
        gap_limit = 5
        sample_limit = 10
        output = []
        gap_holder = []

        for gap in range(1, gap_limit + 1):
            step = gap
            temp_output = []

            for count, entry in enumerate(results):
                if count == step:
                    if len(temp_output) != sample_limit:
                        temp_output.append(entry)
                        step += (gap + 1)
                    else:
                        break

            output.append((f"gap: {gap}", temp_output))

        # [(1, [...]), (2, [...]), (gap, [gap_results_of_10])]
        return output

    # [("0", {"11am": [...]...}), ("1", {"11am": [...]})]
    all_results = get_all_results()
    output = []

    for common_digit, time_results in all_results:
        # {"11am": [...], "4pm": [...], "9pm": [...]}
        new_time_results = {}

        for time, results in time_results.items():
            results = make_gaps(results)
            new_time_results.setdefault(time, [])
            new_time_results[time].extend(results)

        output.append((common_digit, new_time_results))

    # [("0", {...}), ("1", {...}) ...]
    return output


def filter_gap_results():

    def first_two(gap_results):
        output = []
        prev_count = 0
        gap_holder = []

        # results = [("gap: 1", [("561", [], 12, "12 thu dec 2019")]), ...]
        for entry in gap_results:
            # "gap: 1"
            gap_str = entry[0]
            # [("561", [], 12, "12 thu dec 2019")]), ...]
            results = entry[1]
            temp_output = []

            # res = ("561", [], 12, "12 thu dec 2019")
            for count, res in enumerate(results):
                if res[1]:
                    if prev_count == 0:
                        temp_output.insert(0, res)
                        prev_count = count
                    else:
                        if prev_count == count and len(temp_output) != 2:
                            temp_output.insert(0, res)
                        else:
                            prev_count = 0
                            break

                    prev_count += (count + 1)

            if len(temp_output) == 2 and (temp_output not in gap_holder):
                gap_holder.append(temp_output)
                output.append((gap_str, temp_output))
                # prev_count = 0
                # break

        # [("gap: 1", [(...), (...)]), ...]
        return output

    def custom_filter(new_results):
        # Current filter:
        #   a. gap of two
        #   b. same digit

        # [('gap: 1', [...]), ('gap: 2', [...]), ('gap: 3', [...])]
        output = []

        for gap_results in new_results:
            # [("gap: 2", [(...), (...)])]
            digits = list(map(
                lambda x: [int(j[-1]) for j in x[1]], gap_results[1]))

            for j in digits[0]:
                for k in digits[1]:
                    if (
                        abs(j - k) == 2
                        or abs(j - k) == 8
                        or abs(j - k) == 0
                    ):
                        digits[1].remove(k)

            if not digits[1]:
                output.append(gap_results)

        return output

    all_gap_results = get_gap_results()
    file_name = Path("get_probables.txt")
    gap_holder = []

    with open(file_name, "w") as fo:
        for common_digit, time_results in all_gap_results:
            for time, gap_results in time_results.items():
                # [("gap: 1", [...]), ...]
                new_results = first_two(gap_results)
                filter_new_results = custom_filter(new_results)

                if filter_new_results:
                    for entry in filter_new_results:
                        print(
                            f"common: {common_digit}, "
                            f"time: {time}, "
                            f"{entry[0]}"
                        )

                        fo.write(
                            f"common: {common_digit}, "
                            f"time: {time}, "
                            f"{entry[0]}\n"
                        )

                        for e in entry[1]:
                            print(f"{e[0]} - {e[1]} - {e[3]}")
                            fo.write(f"{e[0]} - {e[1]} - {e[3]}\n")
                        print("\n")
                        fo.write("\n\n")


def main():
    filter_gap_results()


if __name__ == "__main__":
    main()
