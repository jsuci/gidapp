
from re import split
from itertools import islice, combinations


def get_results(gap):
    results = []
    reversed_res = []

    with open("results_v2.txt", "r") as fi:
        for entry in islice(fi, 2, None):
            result = split(r"\s{2,}", entry.strip())
            reversed_res.insert(0, result)

    for c, e in enumerate(reversed_res):
        if c % gap == 0:
            results.insert(0, e)

    return results[-4:]


def check_num(user_num, my_num):
    fdigits = []

    for num in user_num:
        if num in my_num:
            fdigits.append(num)
            my_num = my_num.replace(num, '', 1)

    return (''.join(fdigits), len(fdigits))


def get_pairs(res_1, res_2):
    pairs = []

    for r1 in res_1[1:]:
        for r2 in res_2[1:]:
            pair = ''.join(sorted(check_num(r1, r2)[0]))

            if len(pair) == 2:
                pairs.append(pair)

            if len(pair) == 3:

                for pr in combinations(pair, 2):
                    pr = ''.join(pr)

                    if pr not in pairs:
                        pairs.append(pr)

    return pairs


def get_pair_res(pf, rs):

    holder = ['---', '---', '---']

    for er in rs:
        ser = [''.join(sorted(x)) for x in combinations(er, 2)]

        if pf in ser:
            ser_index = rs.index(er)
            holder[ser_index] = er

    print(f'{" ":3}'.join(holder))


def main():
    all_gap_pairs = {}
    for gap in range(1, 101):

        res = get_results(gap)

        g_pairs = []
        for i in range(len(res) - 1):
            gp = get_pairs(res[i], res[i + 1])

            g_pairs.append(gp)

        if g_pairs[0] and g_pairs[1]:

            pfound = []
            for g1 in g_pairs[0]:
                if g1 in g_pairs[1]:
                    if g1 not in pfound:
                        pfound.append(g1)

            if len(pfound) >= 1:
                print('gap:', gap)
                print('pair:', pfound)

                for pf in pfound:
                    for e in res:
                        get_pair_res(pf, e[1:])

                    print('\n')

                print('\n')

                for pf in pfound:
                    all_gap_pairs.setdefault(pf, 0)
                    all_gap_pairs[pf] += 1

    print('pairs stats:')
    for k, v in sorted(all_gap_pairs.items(), key=lambda x: x[1]):
        print(k, v)


if __name__ == '__main__':
    main()
