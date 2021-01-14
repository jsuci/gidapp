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


def digit_gap_pair(digit, max_step, results):
    sdigit = str(digit)

    for step in range(1, max_step):
        gap = step
        out_path = Path(f"digit-gap-pair/digit_{digit}_gap_{step}.txt")
        found = []

        with open(out_path, "w") as file_out:

            for line, res in enumerate(results[0:100]):
                if (line == gap) and (sdigit in res):
                    str_res = f"[{res[0]} {res[1]} {res[2]}]"
                    file_out.write(f"{res} {str_res}\n")
                    found.append(res)
                    gap = (gap + 1) + step
                else:
                    file_out.write(f"{res}\n")

        if len(found) >= 3:
            print(f"digit: {sdigit}  gap: {step}  found: {len(found)}")
        else:
            ulink_path = Path(
                f"digit-gap-pair/digit_{digit}_gap_{step}.txt")
            ulink_path.unlink()

        found = []


def filter_results():
    results = read_results()
    max_step = 10

    for p in Path("digit-gap-pair").glob("*.txt"):
        p.unlink()

    for digit in range(10):
        digit_gap_pair(digit, max_step, results)

    print("Done processing.")


def main():
    filter_results()


if __name__ == "__main__":
    main()
