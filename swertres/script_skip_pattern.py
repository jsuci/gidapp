from re import split


def skip_pattern(user_num):
    output = {}

    for i in range(0, 10):
        output.setdefault(str(i), [])

    for dg in user_num[0]:
        if len(output[dg]) == 0:
            output[dg].append('current')

    for skip, res in enumerate(user_num, start=1):
        for dg in res:
            if len(output[dg]) == 0:
                output[dg].append(skip - 1)

    return output


def main():
    user_num = split(r"\s{1,}", input("Enter at least 9 results: ").strip())

    result = skip_pattern(user_num)

    for k, v in result.items():
        print(k, v)


if __name__ == "__main__":
    main()
