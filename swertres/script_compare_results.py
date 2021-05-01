from pathlib import Path
from itertools import islice, combinations
from re import split
from sys import argv


def check_num(user_num, my_num):
    fdigits = []

    for num in user_num:
        if num in my_num:
            fdigits.append(num)
            my_num = my_num.replace(num, '', 1)

    return (''.join(fdigits), len(fdigits))


def main():
    inpt_one = split(r"\s{1,}", input("Enter first seq. of results: "))
    inpt_two = split(r"\s{1,}", input("Enter second seq. of results: "))

    for a in inpt_one:
        for b in inpt_two:
            if check_num(a, b)[1] == 3:
                print(check_num(a, b)[0])


if __name__ == "__main__":
    main()
