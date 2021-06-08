
from re import split
from itertools import islice


def get_results(gap, user_in):
    results = []
    reversed_res = []

    with open("results_v2.txt", "r") as fi:
        for entry in islice(fi, 2, None):
            result = split(r"\s{2,}", entry.strip())
            reversed_res.append(0, result)

    for c, e in enumerate(reversed_res):
        if c % gap == 0:

            new_e = []
            new_e.append(e[0])

            for dg in e[1:]:
                check = check_num(user_in, dg)

                if check[1] >= 1:
                    last_two = ''.join(
                        sorted(dg.replace(user_in, "", 1)))
                    dg = f'{dg} ({user_in}-{last_two})'

                new_e.append(dg)

            results.insert(0, new_e)

    return results[-100:]


def check_num(user_num, my_num):
    fdigits = []

    for num in user_num:
        if num in my_num:
            fdigits.append(num)
            my_num = my_num.replace(num, '', 1)

    return (''.join(fdigits), len(fdigits))


def export_results():
    gap_limit = 6
    sample = 50

    user_num = input("Enter digit to filter: ")

    with open("gap_results_1.txt", "w") as fo:

        for gap in range(1, gap_limit):
            results = get_results(gap, user_num)

            fo.write(f"gap: {gap}\n")

            for e in results:
                fo.write(
                    f"{e[0]:<20}{e[1]:<15}"
                    f"{e[2]:<15}{e[3]:<15}\n")

            fo.write(f"\n\n")


def main():
    export_results()


if __name__ == '__main__':
    main()
