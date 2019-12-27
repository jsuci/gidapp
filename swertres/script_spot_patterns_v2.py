from pathlib import Path
from itertools import islice


def read_results():
    result_file = Path("results_v1.txt")
    output = []

    with open(result_file, "r") as fi:
        for result in islice(fi, 2, None):
            result = result.strip()
            output.insert(0, result)

    return output


def gap_results():
    all_results = read_results()
    output = {}
    sample_limit = 3
    gap_limit = 10

    for gap in range(1, gap_limit + 1):
        step = gap
        output.setdefault(gap, [])

        for count, result in enumerate(all_results):
            if count == step:
                if len(output[gap]) != sample_limit:
                    output[gap].append(result)
                    step += (gap + 1)
                else:
                    break

    return output


def filter_gaps():
    def check_common(results):
        common_digits = []

        for common in range(0, 10):
            common = str(common)
            count = 0

            for res in results:
                if common in res:
                    count += 1

            if count == len(results):
                common_digits.append(common)

        return sorted(common_digits)

    dic_gap_results = gap_results()
    control = False

    with open("spot_patterns_v2.txt", "w") as fo:

        for gap, results in dic_gap_results.items():
            common_digits = check_common(results)

            if len(common_digits) == 1:
                common_pair = check_common([results[0], results[-1]])

                if len(common_pair) == 2:
                    print(f"gap: {gap:<5} common: {common_digits[0]}")

                    for res in results:
                        print(res)

                    print(f"\n")

    #         if len(check_common(results)) == 1:
    #             print(f"gap: {gap}")
    #             fo.write(f"gap: {gap}\n")

    #             common_digits = check_common(results)

    #             for result in reversed(results):
    #                 temp_res = result

    #                 for common in common_digits:
    #                     temp_res = temp_res.replace(common, "", 1)

    #                 if len(common_digits) == 1:
    #                     print(
    #                         f"{result} - [{temp_res[0]}] "
    #                         f"[{common_digits[0]:<3}{common_digits[1]}]"
    #                     )

    #                     fo.write(
    #                         f"{result} - [{temp_res[0]}] "
    #                         f"[{common_digits[0]:<3}{common_digits[1]}]\n"
    #                     )
    #                 elif len(common_digits) == 1:
    #                     print(
    #                         f"{result} - [{temp_res[0]:<3}{temp_res[1]}] "
    #                         f"[{common_digits[0]}]"
    #                     )

    #                     fo.write(
    #                         f"{result} - [{temp_res[0]:<3}{temp_res[1]}] "
    #                         f"[{common_digits[0]}]\n"
    #                     )
    #                 else:
    #                     print(
    #                         f"{result} - [{common_digits[0]:<3}"
    #                         f"{common_digits[1]:<3}{common_digits[2]}]"
    #                     )

    #                     fo.write(
    #                         f"{result} - [{common_digits[0]:<3}"
    #                         f"{common_digits[1]:<3}{common_digits[2]}]"
    #                     )

    #             print("\n")
    #             fo.write("\n\n")

    #             control = True

    # return control


def main():
    filter_gaps()


if __name__ == "__main__":
    main()
