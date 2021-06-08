from re import split


def main():
    user_num = split(r"\s+", input("Enter results: "))
    output = {}

    for each_res in user_num:
        each_res = "".join(sorted(each_res))
        output.setdefault(each_res, 0)
        output[each_res] += 1

    for k, v in sorted(output.items(), key=lambda x: x[1]):
        print(k, "->", v)


if __name__ == "__main__":
    main()
