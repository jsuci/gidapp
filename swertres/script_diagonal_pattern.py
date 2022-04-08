from re import split
from itertools import islice
from sys import argv


def get_results():
    results = []

    with open("results_v2.txt", "r") as fi:
        for entry in islice(fi, 2, None):
            result = split(r"\s{2,}", entry.strip())
            results.append(result)

    return results


def compare_res(r1, r2, usr):
    r1 = r1[1:]
    r2 = r2[1:]

    hasR1 = False
    hasR2 = False

    for i in range(3):
        if ('-' in r1[i]) or ('-' in r2[i]):
            break
        else:
            print(r1, r2, usr)


def main():
    res = get_results()
    usr = argv[1:]

    for i in range(len(res[0:3000]) - 1):
        r1 = res[i]
        r2 = res[i + 1]

        validR1 = list(filter(lambda x: '-' in x, r1))
        validR2 = list(filter(lambda x: '-' in x, r2))

        if (len(validR2) == 0) and (len(validR2) == 0):
            print(r1, r2)


if __name__ == "__main__":
    main()
