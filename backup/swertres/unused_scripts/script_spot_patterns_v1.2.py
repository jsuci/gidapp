from pathlib import Path
from itertools import islice
from datetime import datetime


def read_results():
    result_file = Path("results_v1.txt")
    output = []

    with open(result_file, "r") as fi:
        for result in islice(fi, 2, None):
            result = result.strip()
            output.insert(0, result)

    return output


def gap_results(sample_limit):
    all_results = read_results()
    output = {}
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


def filter_gaps(sample_limit):

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

    dic_gap_results = gap_results(sample_limit)
    control = False

    with open("spot_patterns_v1.2.txt", "a") as fo:

        for gap, results in dic_gap_results.items():

            common_digits = check_common(results)

            if len(common_digits) >= 1:
                print(f"gap: {gap}, common: {common_digits}")
                fo.write(f"gap: {gap}, common: {common_digits}\n")

                for result in reversed(results):
                    temp_res = result

                    for common in common_digits:
                        temp_res = temp_res.replace(common, "", 1)

                    print(f"{result}")
                    fo.write(f"{result}\n")

                print("\n")
                fo.write("\n\n")

                control = True

    return control


def main():
    # minimum limit of results
    sample_limit = 3
    date_now = datetime.now()

    with open("spot_patterns_v1.2.txt", "a") as fo:
        fo.write(f"""{date_now.strftime("%c")}\n""")

    while True:
        if filter_gaps(sample_limit):
            sample_limit += 1
        else:
            break


if __name__ == "__main__":
    main()
