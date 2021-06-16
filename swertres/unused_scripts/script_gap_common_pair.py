
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

    return results[-9:]


def check_num(user_num, my_num):
    fdigits = []

    for num in user_num:
        if num in my_num:
            fdigits.append(num)
            my_num = my_num.replace(num, '', 1)

    return (''.join(fdigits), len(fdigits))


def main():
    for gap in range(1, 21):

        res = get_results(gap)

        common_pairs = {}
        for i in range(len(res) - 1):

            pair_entry = []
            for j in res[i][1:]:
                for k in res[i + 1][1:]:

                    if check_num(j, k)[1] == 2:
                        pair = ''.join(sorted(check_num(j, k)[0]))
                        # common_pairs.setdefault(gap, [])
                        # common_pairs[gap].insert(0, pair)
                        pair_entry.append(pair)

                    if check_num(j, k)[1] == 3:
                        pairs = combinations(k, 2)

                        for pr in pairs:
                            pair = ''.join(sorted(pr))
                            # common_pairs.setdefault(gap, [])
                            # common_pairs[gap].insert(0, pair)
                            pair_entry.append(pair)

            if pair_entry:
                common_pairs.setdefault(gap, [])
                common_pairs[gap].extend(pair_entry)

        # f_gap_pairs = {}

        for k, v in common_pairs.items():
            # if v >= 3:
            #     f_gap_pairs.setdefault(gap, [])
            #     f_gap_pairs[gap].append((k, v))
            print(k, v)

        # for k, lst in f_gap_pairs.items():
        #     print(f'gap: {gap}')

        #     for p, c in lst:
        #         print(p, c)

            print('\n')


if __name__ == '__main__':
    # main()
    for e in get_results(5):
        print(e)
