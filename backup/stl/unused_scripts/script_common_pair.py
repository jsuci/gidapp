from itertools import islice, combinations
from re import split


def get_results():
    output = []

    with open("results_v2.txt", "r") as fi:
        for entry in islice(fi, 2, None):
            entry = split(r"\s{2,}", entry.strip())

            output.append(entry)

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


def get_common_pair():
    num_search = split(r"\s+", input("Enter number(s) to search: "))

    top_pairs = []
    all_top_pairs = {}

    with open("common_pair.txt", "w") as fo:
        for num in num_search:
            # print(f"Common pair for {num}")
            fo.write(f"Common pair for {num}\n")

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

            for pair, count in sorted(output.items(), key=lambda x: x[1]):
                # print(f"{pair} ({count})")
                fo.write(f"{pair} ({count})\n")

            # Accumulate each number's top pair
            top_pairs.append(sorted(output.items(), key=lambda x: x[1])[-1])

            # print(f"\n")
            fo.write(f"\n\n")

        # Sort by count
        sorted_all_top_pairs = sorted(
            all_top_pairs.items(), key=lambda x: x[1], reverse=False)

        fo.write("Common pair for all numbers:\n")

        for pair, count in sorted_all_top_pairs:
            fo.write(f"{pair} ({count})\n")

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


def main():
    get_common_pair()


if __name__ == "__main__":
    main()
