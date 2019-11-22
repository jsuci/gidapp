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


def match_results(num_one, num_two):
    output = []

    if 2 <= len(num_one) <= 3:
        for digit in num_one:
            if digit in num_two:
                output.append(digit)
                num_two = num_two.replace(digit, "", 1)

    len_out = len(output)

    if len_out:
        return "".join(sorted(output))
    else:
        return None


def pair_results():
    num_pair = input("Enter a digit to match: ")
    results = get_all_date_results()
    output = []

    for entry in results:
        new_entry = []

        for item in entry:
            digit_item = match_results(item, num_pair)

            if digit_item and len(digit_item) == 1:
                fdigit_item = "".join(sorted(item.replace(digit_item, "", 1)))
                new_entry.append(f"{item} ({digit_item}-{fdigit_item})")
            else:
                new_entry.append(item)

        output.append(new_entry)

    return output


def export_results(results):
    # gap_limit = int(input("Enter gap limit: "))
    gap_limit = 6
    # sample = int(input("Enter number of samples: "))
    sample = 50

    with open("digit_results_v2.txt", "w") as fo:

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
    new_results = pair_results()
    export_results(new_results)


if __name__ == "__main__":
    main()
