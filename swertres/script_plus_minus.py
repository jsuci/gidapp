from itertools import combinations, product


def plus_minus(prev_res):
    # all_e = []
    sum_e = []
    minus_e = []

    for e in combinations(prev_res, 2):
        sum_val = sum(e) % 10 if sum(e) < 11 else None
        minus_val = abs(e[0] - e[1])

        if (
            sum_val is not None
            # and sum_val not in all_e
            and sum_val not in prev_res
        ):
            # all_e.append(sum_val)
            sum_e.append(sum_val)

        if (
            minus_val is not None
            # and minus_val not in all_e
            and minus_val not in prev_res
        ):
            # all_e.append(minus_val)
            minus_e.append(minus_val)

    print(f"Plus Digits:\n{sum_e}\n\nMinus Digits:\n{minus_e}")

    # for e in product(prev_res, sum_e, minus_e):
    #     print("".join([str(x) for x in e]), end=" ")

    # for e in prev_res:
    #     if e not in all_e:
    #         for f in product([e], sum_e, minus_e):
    #             print("".join([str(x) for x in f]), end=" ")


def main():
    prev_res = [int(x) for x in input("Enter previous result: ")]
    plus_minus(prev_res)


if __name__ == "__main__":
    main()
