from itertools import combinations


def get_total_combi():
    with open("total_combi_all.txt", "r") as fo:
        return sorted(map(lambda x: x.strip(), fo))


def filter_pairs():
    results = get_total_combi()
    combis = input("Enter a list of combinations: ")

    output = []
    all_pairs = []

    combis = combis.split(" ")

    for combi in combis:
        pairs = (list(map(lambda x: "".join(sorted(x)),
                          combinations(combi, 2))))
        all_pairs.extend(pairs)

    all_pairs = set(all_pairs)

    for res in results:
        s_res = "".join(sorted(res))
        for pair in all_pairs:
            s_pair = "".join(sorted(pair))
            if s_pair in s_res:
                output.append(res)

    with open("total_combo_filtered.txt", "w") as fo:
        for e in sorted(output):
            print(f"{e}")
            fo.write(f"{e}\n")


def filter_one_digit():
    results = get_total_combi()
    digits = set(input("Enter a 3-digit combination: "))

    output_one = []
    output_two = []

    for res in results:
        count = []

        for digit in digits:
            if digit in res:
                count.append(digit)

        if len(set(count)) == 1:
            output_one.append(res)

    print(output_one)

    filter_more = input("Filter further? y/n: ")

    if filter_more == "y":
        digits = input("Enter a 3-digit combination: ")

        for res in output_one:
            count = []

            for digit in digits:
                if digit in res:
                    count.append(digit)

            if len(set(count)) == 1:
                output_two.append(res)

        with open("total_combo_filtered.txt", "w") as fo:
            for e in sorted(output_two):
                print(f"{e}")
                fo.write(f"{e}\n")

    else:
        with open("total_combo_filtered.txt", "w") as fo:
            for e in sorted(output_one):
                print(f"{e}")
                fo.write(f"{e}\n")


def filter_two_digits():
    results = get_total_combi()
    digits = input("Enter a 3-digit combination: ")

    output = []

    for res in results:
        count = 0

        for digit in set(digits):
            if digit in set(res):
                count += res.count(digit)

        if count == 2:
            output.append(res)

    with open("total_combo_filtered.txt", "w") as fo:
        for e in sorted(output):
            print(f"{e}")
            fo.write(f"{e}\n")


def no_filter_digit():
    results = get_total_combi()
    digits = input("Enter a 3-digit combination: ")

    output = []

    for res in results:
        count = 0

        for digit in set(digits):
            if digit in set(res):
                count += res.count(digit)

        if count == 0:
            output.append(res)

    with open("total_combo_filtered.txt", "w") as fo:
        for e in sorted(output):
            print(f"{e}")
            fo.write(f"{e}\n")


def filter_total_combi():
    user_select = input(
        "Type \"0\" to match pairs from given combinations.\n"
        "Type \"1\" to match atleast 1 digit from given combi.\n"
        "Type \"2\" to match atleast 2 digit from given combi.\n"
        "Type \"3\" to not match any digit from given combi: ")

    if user_select == "0":
        filter_pairs()
    elif user_select == "1":
        filter_one_digit()
    elif user_select == "2":
        filter_two_digits()
    elif user_select == "3":
        no_filter_digit()
    else:
        print("Invalid Option")


def main():
    filter_total_combi()


if __name__ == "__main__":
    main()
