from itertools import *


def high_low_mix(digit):
    low_count = 0
    high_count = 0

    for num in digit:
        if int(num) < 5:
            low_count += 1
        else:
            high_count += 1

    with open("results_high_low_v1.1.txt", "a") as fo:
        if low_count == 3:
            fo.write("{} <- {}\n".format(digit, "low"))
        elif high_count == 3:
            fo.write("{} <- {}\n".format(digit, "high"))
        else:
            fo.write("{} <- {}\n".format(digit, ""))


def main():
    with open("results_high_low_v1.1.txt", "w") as fo:
        fo.write("")

    with open("results_v1.txt", "r") as fi:
        for entry in islice(fi, 2, None):
            digit = entry.strip()
            high_low_mix(digit)


if __name__ == "__main__":
    main()
