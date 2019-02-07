import re
from itertools import islice, combinations
from pathlib import Path

def get_output(to_skip):
    for outer_count in range(20):
        with open("results_v2.txt", "r") as f1:
            step = outer_count + to_skip
            num_match = 0
            fix_ordering = []

            for count, line in enumerate(list(islice(f1, 2, None))[::-1]):
                date_digits = re.split(r"\s{2,}", line.strip())
                per_line = ["{:15}".format(date_digits[0])]
                
                if count == step and num_match != 3:
                    
                    for digit in date_digits[1:]:
                        pair_combi = ["".join(x) for x in combinations(
                            sorted(digit), 2)]
                        per_line_item = "{:27}".format(
                            digit + " " + str(pair_combi))

                        per_line.append(per_line_item)


                    num_match += 1
                    step += (outer_count + 1)
                else:
                    for digit in date_digits[1:]:
                        per_line_item = "{:27}".format(digit)
                        per_line.append(per_line_item)

                fix_ordering.insert(0, "".join(per_line).strip())

            filename = "pair_digits_v2"
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