from re import split
from itertools import islice


def get_all_date_results():
    """
    INPUT:
        results_v2.txt - text file containing all the date and results

    OUTPUT:
        output - a list of date and results (ex. [["02 wed jan 2013", "473",
        "328"]])
    """

    output = []

    with open("results_v2.txt", "r") as file:
        for entry in islice(file, 2, None):
            entry = split(r"\s{2,}", entry.strip())

            output.append(entry)

    return output


def sum_results():
    results = get_all_date_results()
    output = []

    for entry in results:
        new_entry = []

        for item in entry:
            try:
                sum_item = sum(map(lambda x: int(x), item))
                new_entry.append(f"{item} ({sum_item})")
            except Exception:
                new_entry.append(item)

        output.append(new_entry)

    return output


def export_results(results):
    gap_limit = int(input("Enter gap limit: "))
    sample = int(input("Enter number of samples: "))

    with open("sum_results_v2.txt", "w") as fo:

        for gap in range(1, gap_limit):
            step = gap
            rev_results = []

            for count, entry in enumerate(reversed(results)):
                if count == step:
                    rev_results.insert(0, entry)
                    step += (gap + 1)

            fo.write(f"gap: {gap}\n")
            for entry in rev_results[len(rev_results) - sample:]:
                fo.write(
                    f"{entry[0]:<20}{entry[1]:<15}"
                    f"{entry[2]:<15}{entry[3]:<15}\n")
            fo.write(f"\n\n")


def main():
    new_results = sum_results()
    export_results(new_results)


if __name__ == "__main__":
    main()
