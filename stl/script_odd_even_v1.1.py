from itertools import *


def odd_even_mix(digit):
    odd_count = 0
    even_count = 0

    for num in digit:
        if int(num) % 2 == 0:
            even_count += 1
        else:
            odd_count += 1

    with open("results_odd_even_v1.1.txt", "a") as fo:
        if odd_count == 3:
            fo.write("{} <- {}\n".format(digit, "odd"))
        elif even_count == 3:
            fo.write("{} <- {}\n".format(digit, "even"))
        else:
            fo.write("{} <- {}\n".format(digit, ""))


def main():
    with open("results_odd_even_v1.1.txt", "w") as fo:
        fo.write("")

    with open("results_v1.txt", "r") as fi:
        for entry in islice(fi, 2, None):
            digit = entry.strip()
            odd_even_mix(digit)

    print("Done identifying odd, even, mix results.")


if __name__ == "__main__":
    main()
