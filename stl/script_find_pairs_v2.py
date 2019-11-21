from itertools import islice, combinations
from re import split


def all_results():
    output = []

    with open("results_v2.txt", "r") as fi:
        for entry in islice(fi, 2, None):
            entry = split(r"\s{2,}", entry.strip())

            output.append(entry)

    return output


def match_results(num_one, num_two):
    output = []

    if len(num_one) == 3:
        for digit in num_one:
            if digit in num_two:
                output.append(digit)
                num_two = num_two.replace(digit, "", 1)

    len_out = len(output)

    if len_out:
        return "".join(sorted(output))
    else:
        return None


def process_filter(filtered_results, num_two, fi):
    common_results = []
    common_pairs = set()
    sorted_num_two = "".join(sorted(num_two))

    for entry in filtered_results:
        fi.write(f"{entry}\n")
        print(entry)
        for result in entry[1:]:
            sorted_result = "".join(sorted(result))
            sorted_pairs = (list(map(lambda x: "".join(sorted(x)),
                                     combinations(result, 2))))

            if sorted_num_two != sorted_result:
                common_results.append(sorted_result)
                common_pairs.update(sorted_pairs)

    fi.write("\n\n")
    print("\n")

    return [sorted(common_results), sorted(list(common_pairs))]


def ordered_pairs(filtered_results, num_before, num_after, num_two):
    results_only = []

    for entry in filtered_results:
        results_only.extend(entry[1:])

    for i in range(len(results_only) - 1):
        match_num_two = match_results(results_only[i], num_two)
        if match_num_two and (len(match_num_two) == 3):
            match_num_before = match_results(results_only[i - 1], num_before)
            match_num_after = match_results(results_only[i - 1], num_after)

            if match_num_before and len(match_num_before) >= 2:
                return filtered_results
            elif match_num_after and len(match_num_after) >= 2:
                return filtered_results
            else:
                return None


def filter_results():

    num_two = input("Enter base result eg. 146, (510), 438: ")
    num_before = input("Enter before base result eg. (146), 510, 438: ")
    num_after = input("Enter after base result eg. 146, 510, (438): ")
    results = all_results()
    all_filter_results = []
    all_filter_pairs = []
    all_ordered_pairs = []

    dic_all_results = {}
    dic_all_pairs = {}

    with open("find_pairs_v2.txt", "w") as fi:
        print("matched results:")
        fi.write("matched results:\n")

        for i in range(len(results) - 1):
            for entry in results[i]:
                has_match = match_results(entry, num_two)
                if has_match and (len(has_match) == 3):
                    filtered_results = [results[i - 1],
                                        results[i], results[i + 1]]

                    ordered_pairs_results = ordered_pairs(
                        filtered_results, num_before, num_after, num_two)

                    combine_results = process_filter(
                        filtered_results, num_two, fi)

                    all_filter_results.extend(combine_results[0])
                    all_filter_pairs.extend(combine_results[1])

                    if ordered_pairs_results:
                        all_ordered_pairs.extend(ordered_pairs_results)
                        all_ordered_pairs.append("\n")

        for e in all_filter_results:
            dic_all_results[e] = dic_all_results.get(e, 0) + 1

        for e in all_filter_pairs:
            dic_all_pairs[e] = dic_all_pairs.get(e, 0) + 1

        print(f"ordered pairs:")
        fi.write(f"ordered pairs:\n")

        for e in all_ordered_pairs:
            if e == "\n":
                print(f"\n\n")
                fi.write(f"\n\n")
            else:
                print(f"{e}")
                fi.write(f"{e}\n")

        print(f"common results and pairs:")
        fi.write(f"common results and pairs:\n")

        fi.write(
            f"{sorted(dic_all_results.items(), key=lambda x: x[1])[-5:]}\n")
        fi.write(
            f"{sorted(dic_all_pairs.items(), key=lambda x: x[1])[-5:]}")

        print(
            f"{sorted(dic_all_results.items(), key=lambda x: x[1])[-5:]}")
        print(
            f"{sorted(dic_all_pairs.items(), key=lambda x: x[1])[-5:]}")


def main():
    filter_results()


if __name__ == "__main__":
    main()
