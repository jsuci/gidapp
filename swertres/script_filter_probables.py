from re import search
from itertools import combinations, repeat


def get_probables():
    """Get all the probables with corresponding date. Return a dictionary of
    {date: [probables]}"""

    dates = []
    digits = []
    all_digits = []

    with open("my_probables_v2.3.txt") as f1:
        for line in f1:
            entry = line.strip()
            check_date = search(r"(?<=date: )([0-9a-zA-Z ])+", entry)
            check_digits = search(r"^\d\d\d$", entry)

            if check_date:
                dates.append(check_date.group(0))

                if digits:
                    all_digits.append(digits)
                    digits = []

            if check_digits:
                digits.append(check_digits.group(0))

        else:
            all_digits.append(digits)

    if dates and all_digits:
        date_digits = list(zip(dates, all_digits))

        return (date_digits)


def digits_match(res, combi):
    """Returns True if the given res("123") does contain any pair
    combiantions from combi("342")"""

    for digit in combi:
        if digit in res:
            res = res.replace(digit, "", 1)

    if len(res) == 1 or len(res) == 0:
        return True
    else:
        return False


def filter_probs(days, combi):
    """Given a days(5) int value and a string combi("123") determine
    all the possible probables starting from the given days. Return a list of
    probables"""

    date_probables = get_probables()[-days:]

    for date, probs in date_probables:
        probs_matches = list(filter(lambda x: digits_match(x, combi), probs))

        if probs_matches:
            print(date, probs_matches)


def main():
    days = int(input("Enter how many days from the current result: "))
    combi = input("Enter count missing combinations: ")

    filter_probs(days, combi)


if __name__ == "__main__":
    main()
