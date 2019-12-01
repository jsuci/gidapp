from re import split


def get_results():
    output = []

    with open("common_combi.txt", "r") as fi:
        for entry in fi:
            if len(entry) != 0:
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


def by_pair(results, u_pairs):
    u_pairs = split(r"\s+", u_pairs)
    output = []

    for pair in u_pairs:
        output.extend(filter(
            lambda x: has_a_match(x[:3], pair), results
        ))

    with open("filter_combi.txt", "w") as fi:
        print(f"Filter by pairs:")
        fi.write(f"Filter by pairs:\n")

        for combi in output:
            print(f"{combi}")
            fi.write(f"{combi}\n")


def by_sum(results, u_sum):
    u_sum = split(r"\s+", u_sum)
    output = []

    for e_sum in u_sum:
        output.extend(filter(
            lambda x: sum(map(lambda y: int(y), x[:3])) == int(e_sum), results
        ))

    with open("filter_combi.txt", "w") as fi:
        print(f"Filter by sum:")
        fi.write(f"Filter by sum:\n")

        for combi in output:
            print(f"{combi}")
            fi.write(f"{combi}\n")


def by_combi(results, u_combi):
    u_combi = split(r"\s+", u_combi)
    output = []

    for combi in u_combi:
        output.extend(filter(
            lambda x: has_a_match(x[:3], combi) == 3, results
        ))

    with open("filter_combi.txt", "w") as fi:
        print(f"Filter by combi:")
        fi.write(f"Filter by combi:\n")

        for combi in output:
            print(f"{combi}")
            fi.write(f"{combi}\n")


def filter_combi():
    all_results = get_results()
    user_input = int(input(
        f"Enter 0 to filter by pairs\n"
        f"Enter 1 to filter by sum\n"
        f"Enter 2 to filter by combi: "))

    if user_input == 0:
        u_pairs = input("Enter pairs (eg. 12 34 56): ")
        by_pair(all_results, u_pairs)

    elif user_input == 1:
        u_sum = input("Enter sum (eg. 00 10 27): ")
        by_sum(all_results, u_sum)

    elif user_input == 2:
        u_count = input("Enter combi (eg, 123 345): ")
        by_combi(all_results, u_count)

    else:
        print(f"Invalid option")


def main():
    filter_combi()


if __name__ == "__main__":
    main()
