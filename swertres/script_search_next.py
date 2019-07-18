from re import split
from itertools import islice


def get_all_date_results():
    """
    INPUT:
        results_v2.txt - text file containing all the date and results

    OUTPUT:
        output - a list of date and results (ex. ["02 wed jan 2013", "473",
        "328"])
    """

    output = []

    with open("results_v2.txt", "r") as file:
        for entry in islice(file, 2, None):
            entry = split(r"\s{2,}", entry.strip())

            output.extend(entry)

    return output


def digits_match(res, combi):
    """
    INPUT:
        res - a string of 3 digit numbers (ex. "123") taken from results_v2.txt
        combi - a string of 3 digit numbers (ex. "321") taken from the user

    OUTPUT:
        True or False - return a boolean value. True if all digits match and
        False if is not
    """

    for digit in combi:
        if digit in res:
            res = res.replace(digit, "", 1)

    if not res:
        return True
    else:
        return False


def search_next():
    """
    INPUT:
        all_date_results - a list of date and results (ex. ['28 mon jan 2013',
        '760', '628']) taken from results_v2.txt
        combi - a string of 3 digit numbers (ex. "670") from user input

    OUTPUT:
        output - a list of list of date and results (ex. [['28 mon jan 2013',
        '760', '628']])
    """

    all_date_results = get_all_date_results()
    combi = input("Enter previous 3 digit combination: ")
    output = []
    temp = []
    curr_date = ""
    found = False

    for c, res in enumerate(all_date_results):
        len_res = len(res)

        if len(temp) == 3:
            output.append(temp)
            temp = []
            found = False
        else:
            if len(res) > 3:
                curr_date = res
                continue

            if len_res == 3 and digits_match(res, combi):
                temp.insert(0, curr_date)
                found = True

            if found:
                temp.append(res)

    with open("results_search_next.txt", "w") as file:
        for entry in output:
            print(f"{entry}")

            file.write(f"{entry}\n")


def main():
    search_next()


if __name__ == "__main__":
    main()
