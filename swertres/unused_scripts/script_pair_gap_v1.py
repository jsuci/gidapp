from pathlib import Path
from itertools import islice


def read_results():
    result_file = Path("results_v1.txt")
    output = []

    with open(result_file, "r") as fi:
        for result in islice(fi, 2, None):
            result = result.strip()
            output.append(result)

    return output


def has_pairs(num_1, num_2):
    pair = []

    for digit in num_1:
        if (digit in num_2) and (digit not in pair):
            pair.append(digit)

    if len(pair) == 2:
        return pair


def gap_check(gap, num_1, results):
    out_path = Path(f"gap-pair/gap_pair_{gap}.txt")
    output = []

    for num_2 in results:
        pair = has_pairs(num_1, num_2)
        if pair:
            output.append(f"{num_2}\t[{pair[0]} {pair[1]}]")
        else:
            output.append(num_2)

    with open(out_path, "w") as file_out:
        for e in output:
            file_out.write(f"{e}\n")


def filter_results():
    results = read_results()
    rev_results = list(reversed(read_results()))
    max_gap = 10

    for p in Path("gap-pair").glob("*.txt"):
        p.unlink()

    for i in range(1, max_gap + 1):
        num_1 = rev_results[i]
        gap_check(i, num_1, results)

    print("Done processing.")


def main():
    filter_results()


if __name__ == "__main__":
    main()
