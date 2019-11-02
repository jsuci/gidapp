from itertools import combinations


def get_total_combi():
    with open("total_combi_all.txt", "r") as fo:
        return sorted(map(lambda x: x.strip(), fo))


def filter_zero(results):
    digits = set(input("Enter series of digits (eg. 1234): "))
    output = []

    for res in results:
        matches = set()

        for digit in digits:
            if digit in set(res):
                matches.add(digit)

        if len(matches) == 0:
            output.append(res)

    return output


def filter_one(results):
    digits = set(input("Enter series of digits (eg. 1234): "))
    output = []

    for res in results:
        matches = set()

        for digit in digits:
            if digit in res:
                matches.add(digit)

        if len(matches) == 1:
            output.append(res)

    return output


def filter_pair(results):
    combis = input("Enter a list of combi (eg. 123 456 789): ").split(" ")

    output = []
    all_pairs = set()

    for combi in combis:
        pairs = (list(map(lambda x: "".join(sorted(x)),
                          combinations(combi, 2))))
        all_pairs.update(pairs)

    for res in results:
        s_res = "".join(sorted(res))
        for pair in all_pairs:
            s_pair = "".join(sorted(pair))
            if s_pair in s_res:
                output.append(res)

    return output


def filter_total_combi():
    user_quit = "n"
    current_results = get_total_combi()

    while user_quit != "y":
        user_select = input(
            "Type \"0\" to match 0 digit from given digits (eg. 1234).\n"
            "Type \"1\" to match 1 digit from given digits (eg. 1234).\n"
            "Type \"2\" to match by pair from given combi (eg. 123 456 789): ")

        print("\n")

        if user_select == "0":
            current_results = filter_zero(current_results)
        elif user_select == "1":
            current_results = filter_one(current_results)
        elif user_select == "2":
            current_results = filter_pair(current_results)
        else:
            print("Invalid option")

        print(f"\n{current_results}\n")

        user_quit = input("Done filtering? (y/n): ")

        print("\n")

    with open("total_combo_filtered.txt", "w") as fo:
        print("Exporting to file...")
        for e in sorted(current_results):
            print(f"{e}")
            fo.write(f"{e}\n")


def main():
    filter_total_combi()


if __name__ == "__main__":
    main()
