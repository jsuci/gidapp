from re import split


def has_pair(num_one, num_two):
    pair = []

    for e1 in num_one:
        if e1 in num_two:
            pair.append(e1)
            num_one = num_one.replace(e1, "", 1)
            num_two = num_two.replace(e1, "", 1)

    if len(pair) >= 2:
        return sorted(pair)
    else:
        return []


def main():
    results = []

    while True:
        user_str = input(
            "Enter previous month results\n"
            "(ex. 478 129 901  896 559 305...): "
        )
        entries = split("\s+", user_str)

        if len(entries) > 1:
            results.append(entries)
        else:
            break

    common_pair = {}

    for e0 in results[0]:
        for j_row in results[1:]:
            for j0 in j_row:
                pair = has_pair(e0, j0)
                # print(e0, j0, pair)
                if len(pair) == 3:
                    common_pair.setdefault(f"{pair[0]}{pair[1]}{pair[2]}", 0)
                    common_pair[f"{pair[0]}{pair[1]}{pair[2]}"] += 1

    for k, v in common_pair.items():
        print(k, v)


if __name__ == "__main__":
    main()
