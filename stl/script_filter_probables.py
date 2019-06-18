from re import search
from itertools import combinations, repeat


def get_probables():
    """Get all the probables with corresponding date. Return a dictionary of
    {date: [probables]}"""

    dates = []
    digits = {}
    all_digits = []
    time = ""

    with open("my_probables_v2.3.txt") as f1:
        for line in f1:
            entry = line.strip()
            check_date = search(r"(?<=date: )([0-9a-zA-Z ])+", entry)
            check_digits = search(r"^\d\d\d$", entry)
            check_time = search(r"(?<=time: )(\d{1,2}(?:a|p)m)", entry)

            if check_time:
                time = check_time.group(0)

            if check_date:
                dates.append(check_date.group(0))

                if digits:
                    all_digits.append(digits)
                    digits = {}

            if check_digits:
                digits.setdefault(time, [])
                digits[time].append(check_digits.group(0))

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

    for entry in date_probables:
        date, time_probs = entry

        for time, probs in time_probs.items():
            has_combi = list(filter(lambda x: digits_match(x, combi), probs))

            if has_combi:
                print(date, {time: has_combi})


def main():
    days = int(input("Enter how many days from the current result: "))
    combi = input("Enter count missing combinations: ")

    filter_probs(days, combi)


if __name__ == "__main__":
    main()
