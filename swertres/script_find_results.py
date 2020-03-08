from itertools import islice
from re import split
from datetime import datetime


def read_results():
    output = []

    with open("results_v2.txt", "r") as fi:
        # updated: 04 sat jan 2020 2
        check_date = fi.readline().strip()[-1]

        for entry in islice(fi, 1, None):
            entry = split(r"\s{2,}", entry.strip())
            entry[0] = datetime.strptime(
                entry[0],
                "%d %a %b %Y"
            ).strftime(
                "%d %B %Y"
            )

            output.append(entry)

        if check_date == "2":
            return output
        else:
            return output[:-1]


def find_results(res):

    def loose_match(res, user_res):
        output = []

        for digit in res:
            if digit in user_res:
                output.append(digit)
                res = res.replace(digit, "", 1)
                user_res = user_res.replace(digit, "", 1)

        if len(output) == 3:
            return True
        else:
            return False

    all_results = read_results()
    found_results = []
    exact = "n"

    for date_res in all_results:
        if exact == "y":
            curr_match = list(filter(
                lambda x: True if x in res else False, date_res[1:]))

            if len(curr_match) >= 2:
                print(date_res)

        else:
            match = []
            for j in date_res[1:]:
                for k in res:
                    if loose_match(k, j):
                        match.append(j)

            if len(match) >= 1:
                found_results.extend(date_res[1:])

    for e in sorted(set([("".join(sorted(x)), found_results.count("".join(sorted(x))))
                         for x in found_results]), key=lambda x: x[1]):
        print(e)


def main():
    res = input("Enter prev results: ").split(" ")
    find_results(res)


if __name__ == "__main__":
    main()
