import re
from itertools import islice

def main():
    outer_count = 2
    with open("results_v2.txt", "r") as f1:
        step = outer_count
        num_match = 0

        for count, line in enumerate(islice(f1, 2, None)):
            digits = re.split(r"\s{10}", line.strip())[1:]

            if count == step:
                print(count, digits, "*")

                num_match += 1
                step += (outer_count + 1)
            else:
                print(count, digits)

if __name__ == "__main__":
    main()