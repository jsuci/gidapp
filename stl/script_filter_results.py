from itertools import islice, product
from pathlib import Path
from re import split


def get_all_results():
    result_file = Path("results_v2.txt")
    output = []

    with open(result_file, "r") as fi:
        for entry in islice(fi, 2, None):
            entry = split(r"\s{2,}", entry.strip())
            output.insert(0, entry)

    return output


def has_a_match(result, num_compare):
    len_result = len(result)
    output = []

    if len_result == 3:
        for digit in result:
            if digit in num_compare:
                output.append(digit)
                result = result.replace(digit, "", 1)
                num_compare = num_compare.replace(digit, "", 1)

    len_output = len(output)

    if len_output == 2 or len_output == 3:
        return len_output
    else:
        return None


def by_common():
    common = input("Enter a common digit: ")
    output = []
    all_results = get_all_results()

    for entry in all_results:
        new_entry = []

        for item in entry:
            if len(item) == 3 and common in item:
                rep_res = item.replace(common, "", 1)
                pairs = sorted(map(lambda x: "".join(x), product(
                    common, rep_res)))
                new_entry.append(f"{item} - {pairs[0]}, {pairs[1]}")
            else:
                new_entry.append(item)

        output.append(new_entry)

    return output


def by_sum():
    all_results = get_all_results()
    output = []

    for entry in all_results:
        new_entry = []

        for item in entry:
            if len(item) == 3:
                item_value = sum([int(x) for x in item])
                new_entry.append(f"{item} - {item_value}")
            else:
                new_entry.append(item)

        output.append(new_entry)

    return output


def by_pair():
    pair = input("Enter a pair: ")
    all_results = get_all_results()
    output = []

    for entry in all_results:
        new_entry = []

        for item in entry:
            if len(item) == 3 and has_a_match(item, pair) == 2:
                temp_item = item
                temp_pair = pair
                for d in temp_pair:
                    if d in temp_item:
                        temp_item = temp_item.replace(d, "", 1)

                new_entry.append(f"{item} {pair} - {temp_item}")
            else:
                new_entry.append(item)

        output.append(new_entry)

    return output


def filter_results():

    filter_opt = input(
        f"Enter 0 to filter by common\n"
        f"Enter 1 to filter by sum\n"
        f"Enter 2 to filter by pair: ")

    if filter_opt == "0":
        return by_common()
    elif filter_opt == "1":
        return by_sum()
    elif filter_opt == "2":
        return by_pair()
    else:
        print("Error command not found.")


def gap_results(all_filter_res):
    gap_limit = int(input("Enter gap limit: "))
    sample_limit = int(input("Enter sample limit: "))
    output = {}

    for gap in range(1, gap_limit + 1):
        step = gap
        temp_output = []

        for count, entry in enumerate(all_filter_res):
            if count == step and len(temp_output) != sample_limit:
                temp_output.insert(0, entry)
                step += (gap + 1)

        output[gap] = temp_output

    return output


def output_results(all_gap_res):
    file_ex = Path("filter_results.txt")

    with open(file_ex, "w") as fe:
        for k, e in all_gap_res.items():
            print(f"gap: {k}")
            fe.write(f"gap: {k}\n")

            for i in e:
                print(f"{i[0]:<20}{i[1]:<15}{i[2]:<15}{i[3]}")
                fe.write(f"{i[0]:<20}{i[1]:<15}{i[2]:<15}{i[3]}\n")

            print("\n")
            fe.write("\n\n")


def main():
    all_filter_res = filter_results()
    all_gap_res = gap_results(all_filter_res)

    output_results(all_gap_res)


if __name__ == "__main__":
    main()
