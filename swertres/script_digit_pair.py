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


def digit_pair(digit, results):
    sdigit = str(digit)
    out_path = Path(f"digit-pair/digit_pair_{digit}.txt")

    with open(out_path, "w") as file_out:
        for res in results:
            sres = sorted(res)

            if sdigit in res:
                sres.remove(sdigit)
                file_out.write(f"{res}\t{digit}\t[{sres[0]} {sres[1]}]\n")
            else:
                file_out.write(f"{res}\n")


def filter_results():
    results = read_results()

    for p in Path("digit-pair").glob("*.txt"):
        p.unlink()

    for digit in range(10):
        digit_pair(digit, results)

    print("Done processing.")


def main():
    filter_results()


if __name__ == "__main__":
    main()
