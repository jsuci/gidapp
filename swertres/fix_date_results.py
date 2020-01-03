from datetime import datetime, timedelta
from itertools import islice
from re import split


def read_results():
    output = []

    with open("results_v2.txt", "r") as fi:
        check_date = fi.readline().strip()[-1]

        for entry in islice(fi, 1, None):
            entry = split(r"\s{2,}", entry.strip())

            output.append(entry)

        if check_date == "2":
            return output
        else:
            return output[:-1]


def date_gap():
    all_results = read_results()

    for i in range(len(all_results) - 1):
        first_date = datetime.strptime(all_results[i][0], "%d %a %b %Y")
        second_date = datetime.strptime(all_results[i + 1][0], "%d %a %b %Y")
        time_diff = second_date - first_date

        if time_diff.days == 1:
            print(all_results[i])
        else:
            print(all_results[i])
            for i in range(1, time_diff.days):
                time_fill = (first_date + timedelta(days=i)
                             ).strftime("%d %a %b %Y")
                print([time_fill, "", "", ""])


def main():
    date_gap()


if __name__ == "__main__":
    main()
