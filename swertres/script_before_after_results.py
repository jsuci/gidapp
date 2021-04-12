from pathlib import Path


def get_results():
    result_path = Path('results_v2.txt')
    output = []

    with open(result_path, 'r') as f:
        for line in f:
            results = line.strip().split()[4:]

            output.extend(results)

    return output


def check_num(user_num, my_num):
    count = 0

    for num in user_num:
        if num in my_num:
            count += 1
            my_num = my_num.replace(num, '', 1)

    if count == 1:
        return "one"
    elif count == 2:
        return "two"
    elif count == 3:
        return "three"
    else:
        return "zero"


def main():
    results = get_results()
    collect = []
    classify = {}

    for count, num in enumerate(results):
        if (
            check_num('650', num) == 'three'
            and (count != 0 or count != len(results) + 1)
        ):
            before_num = results[count - 1]
            after_num = results[count + 1]

            collect.extend([before_num, after_num])

    for num in collect:
        num = ''.join(sorted(num))
        classify.setdefault(num, 0)
        classify[num] += 1

    for k, v in classify.items():
        if v >= 3:
            print(k, v)


if __name__ == "__main__":
    main()
