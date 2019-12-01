from re import split, match


def get_results():
    output = []

    with open("common_combi.txt", "r") as fi:
        for entry in fi:
            if not match(r"\n", entry):
                entry = entry.strip()
                output.append(entry)
            else:
                break

    return output


def has_a_match(result, num_compare):
    len_result = len(result)
    output = []

    if len_result == 3:
        for digit in result:
            if digit in num_compare:
                output.append(digit)
                result = result.replace(digit, "", 1)
                num_compare = num_compare.replace(digit, "", 1)

    len_output = len(output)

    if len_output == 2 or len_output == 3:
        return len_output
    else:
        return None


def include_pair(results, u_pairs):
    u_pairs = split(r"\s+", u_pairs)
    output = []

    for pair in u_pairs:
        output.extend(filter(
            lambda x: has_a_match(x[:3], pair), results
        ))

    return output


def exclude_pair(results, u_pairs):
    u_pairs = split(r"\s+", u_pairs)

    for pair in u_pairs:
        results = list(
            filter(
                lambda x: True if not has_a_match(
                    x[:3], pair) else False, results
            ))

    return results


def by_sum(results, u_sum):
    u_sum = split(r"\s+", u_sum)
    output = []

    for e_sum in u_sum:
        output.extend(filter(
            lambda x: sum(map(lambda y: int(y), x[:3])) == int(e_sum), results
        ))

    return output


def by_combi(results, u_combi):
    u_combi = split(r"\s+", u_combi)
    output = []

    for combi in u_combi:
        output.extend(filter(
            lambda x: has_a_match(x[:3], combi) == 3, results
        ))

    return output


def include_digit(results, u_digit):
    u_digit = split(r"\s+", u_digit)
    output = []

    for digit in u_digit:
        output.extend(filter(
            lambda x: digit in x[:3], results))

    return output


def exclude_digit(results, u_digit):
    u_digit = split(r"\s+", u_digit)

    for digit in u_digit:

        # Exclude each digit from existing results
        results = list(filter(
            lambda x: True if digit not in x[:3] else False, results))

    return results


def filter_combi():
    all_results = get_results()
    quit_filter = ""

    while quit_filter != "y":

        user_input = int(input(
            f"Enter 0 to include pairs(s)\n"
            f"Enter 1 to exclude pairs(s)\n"
            f"Enter 2 to filter by sum(s)\n"
            f"Enter 3 to filter by combi(s)\n"
            f"Enter 4 to include digit(s)\n"
            f"Enter 5 to exclude digit(s): "))

        print(f"\n")

        if user_input == 0:
            u_pairs = input("Enter pair(s) (eg. 12 34 56): ")
            all_results = include_pair(all_results, u_pairs)

        elif user_input == 1:
            u_pairs = input("Enter pair(s) (eg. 12 34 56): ")
            all_results = exclude_pair(all_results, u_pairs)

        elif user_input == 2:
            u_sum = input("Enter sum(s) (eg. 00 10 27): ")
            all_results = by_sum(all_results, u_sum)

        elif user_input == 3:
            u_count = input("Enter combi(s) (eg. 123 345): ")
            all_results = by_combi(all_results, u_count)

        elif user_input == 4:
            u_digit = input("Enter digit(s) (eg. 1 3 5): ")
            all_results = include_digit(all_results, u_digit)

        elif user_input == 5:
            u_digit = input("Enter digit(s) (eg. 1 3 5): ")
            all_results = exclude_digit(all_results, u_digit)

        else:
            print(f"Invalid option")
            break

        # Remove duplicate entries
        all_results = set(all_results)

        with open("filter_combi.txt", "w") as fo:
            for e in sorted(all_results):
                print(f"{e}")
                fo.write(f"{e}\n")

        print(f"\n")

        quit_filter = input("Done filtering? y/n: ")

        print(f"\n")


def main():
    filter_combi()


if __name__ == "__main__":
    main()
