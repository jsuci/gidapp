from pathlib import Path
from re import split
from sys import argv


def get_results():
    result_path = Path('results_v2.txt')
    output = []

    with open(result_path, 'r') as f:
        for line in f:
            results = split(r"\s{2,}", line.strip())

            output.append(results)

    return output


def check_num(user_num, my_num):
    fdigits = []

    for num in user_num:
        if num in my_num:
            fdigits.append(num)
            my_num = my_num.replace(num, '', 1)

    return (''.join(fdigits), len(fdigits))


def has_next(date, user_num_lst, res_lst):
    count = 0

    for e_unmlst in user_num_lst:
        for e_reslst in res_lst:
            nxt = check_num(e_unmlst, e_reslst)

            if nxt[1] == 3:
                count += 1

    if count == 2:
        print(date, res_lst)


def main():
    user_lst = argv

    for res in get_results():
        date = res[0]
        res_lst = res[1:]

        has_next(date, user_lst, res_lst)


if __name__ == "__main__":
    main()
