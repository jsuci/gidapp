from re import split
from pathlib import Path


def skip_pattern(user_num):
    output = {}

    for i in range(0, 10):
        output.setdefault(str(i), '')

    for dg in user_num[0]:
        if output[dg] == '':
            output[dg] = 'current'

    for skip, res in enumerate(user_num, start=1):
        for dg in res:
            if output[dg] == '':
                output[dg] = skip - 1

    return output


def main():
    contents = []
    fpath = Path("previous_9_results.txt")

    with open(fpath, "r") as f:
        for line in f:
            line = split(r"\s{1,}", line.strip())
            contents.extend(line)

    result = skip_pattern(contents)

    highest_count = 0
    highest = ''
    empty = []

    for k, v in result.items():
        if v == '':
            empty.append(k)
        else:
            if v != 'current' and highest_count < v:
                highest_count = v
                highest = k

    print(f"highest: {highest}\nempty: {empty}")


if __name__ == "__main__":
    main()
