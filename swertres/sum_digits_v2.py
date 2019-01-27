from itertools import islice
from pathlib import Path
import re

def sum_all(digits):
    return str(sum([int(x) for x in digits]))

def get_output(to_skip):
    for outer_count in range(2, 20):
        with open("results_v2.txt") as fo:
            step = outer_count + to_skip
            fix_ordering = []

            for i, e in enumerate(list(islice(fo, 2, None))[::-1]):
                digits =  re.split(r"\s{2,}", e.strip())
                per_line = ["{:20}".format(digits[0])]


                """
                Skip the first n of results then start counting
                as i increases so does step, if both are equal value
                then sum_all that digits
                """
                if i == step:
                    for digit in digits[1:]:
                        output = "{:20}".format(
                            digit + " " + "[" +sum_all(digit) + "]")
                        per_line.append(output)
                    step += (outer_count + 1)
                else:
                    for digit in digits[1:]:
                        output = "{:20}".format(digit)
                        per_line.append(output)

                # Latest results are at the bottom of the file
                fix_ordering.insert(0, "".join(per_line).strip())

            filename = "sum_digits_v2"
            Path(filename).mkdir(parents=True, exist_ok=True)
            p = Path(filename, "{}_{:02}.txt".format(
                "result_gap", outer_count))

            with open(p, "w") as f1:
                for e in fix_ordering:
                    f1.write("{}\n".format(e))

    print("Done. Results are exported to \"{}\" folder".format(
        filename))

def main():
    with open("results_v2.txt", "r") as f1:
        curr_results = f1.readline().strip().split()[-1]
        to_skip = 0

        if curr_results != "2":
            to_skip = 1

        get_output(to_skip)


if __name__ == "__main__":
    main()