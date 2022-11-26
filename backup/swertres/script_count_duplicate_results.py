from re import split


def check_num(user_num, my_num):
    fdigits = []

    for num in user_num:
        if num in my_num:
            fdigits.append(num)
            my_num = my_num.replace(num, '', 1)

    return (''.join(fdigits), len(fdigits))


def main():
    inpt_one = split(r"\s{1,}", input("Enter seq. of results: "))
    count_res = {}

    for rs in inpt_one:
        if len(rs) == 3:
            srs = ''.join(sorted(rs))
            count_res.setdefault(srs, 0)
            count_res[srs] += 1

    for k, v in sorted(count_res.items(), key=lambda x: x[1]):
        print(k, v)


if __name__ == "__main__":
    main()
