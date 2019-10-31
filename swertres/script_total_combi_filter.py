
def get_total_combi():
    with open("total_combi_all.txt", "r") as fo:
        return sorted(map(lambda x: x.strip(), fo))


def get_user_pairs():
    pairs = input("Enter pairs separated by comma or space: ")

    if " " in pairs and "," in pairs:
        return pairs.replace(" ", "").split(",")
    elif "," in pairs:
        return pairs.split(",")
    elif " " in pairs:
        return pairs.split(" ")
    else:
        return []


def filter_pairs():
    results = get_total_combi()
    pairs = get_user_pairs()

    output = []

    for res in results:
        s_res = "".join(sorted(res))
        for pair in pairs:
            s_pair = "".join(sorted(pair))
            if s_pair in s_res:
                output.append(res)

    with open("total_combo_filtered.txt", "w") as fo:
        for e in sorted(output):
            print(f"{e}")
            fo.write(f"{e}\n")


def filter_digits():
    results = get_total_combi()
    digits = input("Enter a 3-digit combination: ")

    output = []

    for res in results:
        count = 0

        for digit in set(digits):
            if digit in set(res):
                count += 1

        if count == 1:
            output.append(res)

    with open("total_combo_filtered.txt", "w") as fo:
        for e in sorted(output):
            print(f"{e}")
            fo.write(f"{e}\n")


def filter_pair_combi():
    results = get_total_combi()
    digits = input("Enter a 3-digit combination: ")

    output = []

    for res in results:
        count = 0

        for digit in set(digits):
            if digit in set(res):
                count += 1

        if count == 2:
            output.append(res)

    with open("total_combo_filtered.txt", "w") as fo:
        for e in sorted(output):
            print(f"{e}")
            fo.write(f"{e}\n")


def filter_total_combi():
    user_select = input(
        "Type \"0\" to filter by custom pairs. Type \"1\" to filter by combi. "
        "Type \"2\" to filter by digit pairs: ")

    if user_select == "0":
        filter_pairs()
    elif user_select == "1":
        filter_digits()
    elif user_select == "2":
        filter_pair_combi()
    else:
        print("Invalid Option")


def main():
    filter_total_combi()


if __name__ == "__main__":
    main()
