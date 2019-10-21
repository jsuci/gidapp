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


def filter_total_combi():
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


def main():
    filter_total_combi()


if __name__ == "__main__":
    main()
