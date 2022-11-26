from itertools import islice, combinations
from re import split
from pathlib import Path


def get_results():
    output = []

    with open("results_v2.txt", "r") as fi:
        check_date = fi.readline().strip()[-1]

        for entry in islice(fi, 1, None):
            entry = split(r"\s{2,}", entry.strip())

            output.append(entry)

        if check_date == "2":
            return output
        else:
            return output[:-1]


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


def search_results(num_search):
    all_results = get_results()
    output = []

    for i in range(len(all_results) - 1):
        for entry in all_results[i]:
            if has_a_match(entry, num_search) == 3:
                has_match_val = has_a_match(entry, num_search)
                output.extend([
                    all_results[i - 1],
                    all_results[i],
                    all_results[i + 1]
                ])

    return output


def get_common_combi(num_search, fo):
    top_combi = []
    all_common_combi = {}

    for num in num_search:
        matched_results = search_results(num)
        common_combi = {}
        s_num_search = "".join(sorted(num))

        for entry in matched_results:
            for e_result in entry[1:]:
                s_e_result = "".join(sorted(e_result))

                # Exclude duplicate and num_search from final common_combi
                if s_e_result != s_num_search:
                    if s_e_result not in common_combi:
                        common_combi.setdefault(s_e_result, 1)
                    else:
                        common_combi[s_e_result] += 1

        # Combine each num_search results to sorted_common_combi
        sorted_common_combi = sorted(
            common_combi.items(), key=lambda x: x[1])

        # Get the top pair for this num_search
        top_combi.append(sorted_common_combi[-1])

        # Combine each num_search results to all_common_combi
        for num, count in sorted_common_combi:
            # Limit to atleast 3 or more appearances
            if count >= 3:
                if num not in all_common_combi:
                    all_common_combi.setdefault(num, count)
                else:
                    all_common_combi[num] += count

    # Process all_common_combi
    by_key_all_common_combi = sorted(
        all_common_combi.items(), key=lambda x: x[0])

    by_val_all_common_combi = sorted(
        all_common_combi.items(), key=lambda x: x[1])

    # Export sorted_all_common_combi for filtering
    for num, count in by_key_all_common_combi:
        # print(f"{num} ({count})")
        fo.write(f"{num} ({count})\n")

    print("\n")
    fo.write(f"\n\n")

    print("Top combi for each number: ")
    fo.write(f"Top combi for each number: \n")

    for combi, count in top_combi:
        print(f"{combi} ({count})")
        fo.write(f"{combi} ({count})\n")

    print("\n")
    fo.write(f"\n\n")

    print("Top 3 combi for all numbers: ")
    fo.write(f"Top 3 combi for all numbers:\n")

    for pair, count in by_val_all_common_combi[-3:]:
        print(f"{pair} ({count})")
        fo.write(f"{pair} ({count})\n")


def get_common_pair(num_search, fo):
    top_pairs = []
    all_top_pairs = {}

    for num in num_search:
        # print(f"Common pair for {num}")
        # fo.write(f"Common pair for {num}\n")

        matched_results = search_results(num)
        all_pairs = []
        output = {}

        for entry in matched_results:
            for each_result in entry[1:]:
                if not has_a_match(each_result, num):
                    all_pairs.extend([
                        "".join(sorted(x))
                        for x in combinations(each_result, 2)])

        for pair in all_pairs:
            if pair not in output:
                output.setdefault(pair, 1)
                all_top_pairs.setdefault(pair, 1)
            else:
                output[pair] += 1
                all_top_pairs[pair] += 1

        # for pair, count in sorted(output.items(), key=lambda x: x[1]):
            # print(f"{pair} ({count})")
            # fo.write(f"{pair} ({count})\n")

        # Accumulate each number's top pair
        top_pairs.append(sorted(output.items(), key=lambda x: x[1])[-1])

        # print(f"\n")
        # fo.write(f"\n\n")

    # Sort by count
    sorted_all_top_pairs = sorted(
        all_top_pairs.items(), key=lambda x: x[1], reverse=False)

    # fo.write("Common pair for all numbers:\n")

    # for pair, count in sorted_all_top_pairs:
    # fo.write(f"{pair} ({count})\n")
    print("\n")
    fo.write(f"\n\n")

    print(f"Top pairs for each numbers:")
    fo.write(f"Top pairs for each numbers:\n")

    for pair, count in top_pairs:
        print(f"{pair} ({count})")
        fo.write(f"{pair} ({count})\n")

    print(f"\n")
    fo.write(f"\n\n")

    print(f"Top 3 pairs for all numbers:")
    fo.write(f"Top 3 pairs for all numbers:\n")

    for pair, count in sorted_all_top_pairs[-3:]:
        print(f"{pair} ({count})")
        fo.write(f"{pair} ({count})\n")


def get_common_combi_pair():
    # get_common_combi_pair()
    # num_search = findall(r"(?<=\s)\d{3}(?!\d)", input(
    #     "Enter number(s) to search: "))
    num_search = get_results()[-1][1:]

    file_name = Path("common_combi_pair.txt")

    with open(file_name, "w") as fo:
        get_common_combi(num_search, fo)
        get_common_pair(num_search, fo)


def main():
    get_common_combi_pair()


if __name__ == "__main__":
    main()
