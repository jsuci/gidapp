from itertools import islice
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


def get_common_combi():
    num_search = split(r"\s+", input("Enter number to search: "))
    top_combi = {}
    all_common_combi = {}

    with open("common_combi.txt", "w") as fo:
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

            sorted_common_combi = sorted(
                common_combi.items(), key=lambda x: x[1])

            for num, count in sorted_common_combi:
                # Filter only common digits greater than 2
                if count >= 3:
                    if num not in all_common_combi:
                        all_common_combi.setdefault(num, count)
                    else:
                        all_common_combi[num] += count

            if sorted_common_combi[-1][0] not in top_combi:
                top_combi.setdefault(
                    sorted_common_combi[-1][0], sorted_common_combi[-1][1])
            else:
                top_combi[sorted_common_combi[-1][0]
                          ] += sorted_common_combi[-1][1]

        for num, count in sorted(
                all_common_combi.items(), key=lambda x: x[1]):
            print(f"{num} ({count})")
            fo.write(f"{num} ({count})\n")

        print("\n")
        fo.write(f"\n\n")

        print("Top combinations for each number: ")
        fo.write(f"Top combinations for each number: \n")

        for combi, count in top_combi.items():
            print(f"{combi} ({count})")
            fo.write(f"{combi} ({count})\n")


def main():
    get_common_combi()


if __name__ == "__main__":
    main()
