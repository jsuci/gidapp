from pathlib import Path
from itertools import islice, combinations
from re import split
from sys import argv


def check_num(user_num, my_num):
    fdigits = []

    for num in user_num:
        if num in my_num:
            fdigits.append(num)
            my_num = my_num.replace(num, '', 1)

    return (''.join(fdigits), len(fdigits))


def get_month_results():
    result_path = Path('results_v2.txt')
    output = {}

    with open(result_path, 'r') as f:
        for line in islice(f, 2, None):
            results = split(r"\s{2,}", line.strip())

            mo_yr = ' '.join(results[0].split()[2:4])
            res = results[1:]

            output.setdefault(mo_yr, [])
            output[mo_yr].append(res)

    return output


def filter_results(samp, fnum, snum):

    fnum_lst = []
    snum_lst = []
    output = []

    for c_prs, prs in enumerate(samp):

        for srs in prs:
            if check_num(fnum, srs)[1] == 3:
                fnum_lst.append(c_prs)

            if check_num(snum, srs)[1] == 3:
                snum_lst.append(c_prs)

    for fnum_loc in fnum_lst:
        for snum_loc in snum_lst:
            gap = abs(fnum_loc - snum_loc) - 1

            if fnum_loc < snum_loc:
                bfr = (fnum_loc - gap) - 1
                aftr = (snum_loc + gap) + 1
            else:
                bfr = (snum_loc - gap) - 1
                aftr = (fnum_loc + gap) + 1

            if bfr >= 0 and samp[bfr] not in output:
                output.append(samp[bfr])

            if aftr < len(samp) and samp[aftr] not in output:
                output.append(samp[aftr])

    return output


def g_has_pairs(lng_lst):

    aggr = []

    for e_lng_lst in lng_lst:
        comb = combinations(e_lng_lst, 2)

        for dres in comb:
            hpairs = check_num(dres[0], dres[1])
            if hpairs[1] >= 2:
                aggr.append((e_lng_lst, ''.join(sorted(hpairs[0]))))
                break

    for e_aggr in sorted(aggr, key=lambda x: x[1]):
        print(e_aggr[0], e_aggr[1])


def g_all_digits(lng_lst):

    opt = input('Enter filter combinations: ')
    out = {}

    for e_lng_lst in lng_lst:
        for dg in e_lng_lst:
            s_dg = ''.join(sorted(dg))

            out.setdefault(s_dg, 0)
            out[s_dg] += 1

    if not opt:
        for k, v in sorted(out.items(), key=lambda x: x[1]):
            print(k, v)
    else:
        opt = split("\s+", opt)
        u_opt = []

        for x in opt:
            s_x = ''.join(sorted(x))
            if s_x not in u_opt:
                u_opt.append(s_x)

        for u_dg in u_opt:
            s_u_dg = ''.join(sorted(u_dg))

            for k, v in out.items():
                if k == s_u_dg:
                    print(k, v)


def main():
    mo_res = get_month_results()
    lng_lst = []

    u_int = split("\s+", input('Enter combinations: '))

    for num in combinations(u_int, 2):

        for k, v in mo_res.items():
            out = filter_results(v, num[0], num[1])

            for item in out:
                if item not in lng_lst:
                    lng_lst.append(item)

    g_has_pairs(lng_lst)
    g_all_digits(lng_lst)


if __name__ == "__main__":
    main()
