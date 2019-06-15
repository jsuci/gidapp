from re import match


def filter_probs(date, combi):
    """Given a date string(dd day mm yyyy) and a string combi("123") determine
    all the possible probables starting from the given date. Return a list of
    probables"""

    with open("my_probables_v2.3.txt") as f1:
        for line in f1:
            entry = line.strip()

            if "date" in entry:
                file_date = entry.replace("date: ", "", 1)
                print(file_date)


def main():
    filter_probs("a", "b")


if __name__ == "__main__":
    main()
