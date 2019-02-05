"""
01 thu mar 2018 (7 steps skip)
353 <- 35
...
577 <- 77
...
053 <- 35
...
665 <- 66 (665 confirmed!)

On 01 thu mar 2018 a pattern was formed base on the common digit of 5.
Every 7 steps there is a 5 and these results that has common digit in
them form an alternating pattern.

What this script will do is that it:
1. given a step value search the entire list of results. stop if the
next gap does not contain any common digit anymore.
2. compile the results found into a list of tuple containing the
gap_value, common_digit, list of common digit
[(7, 5, ['053', '577', '353'])]
"""

from itertools import *


def get_results():
    """Get all the previous result and store it in a list in 
    reverse order.
    """

    results = []
    with open("results_v1.txt", "r") as fi:
        for line in islice(fi, 2, None):
            results.insert(0, line.strip())

    return results


def get_pairs(digit, common):
    """Given any digit and common return combination of pairs
    that has common"""
    result = ()
    for pair in combinations(digit, 2):
        pair = "".join(pair)
        if common in pair:
            new_pair = pair.replace(common, "", 1) + common
            result += (new_pair, )
        # else:
        #     result += (pair, )

    return sorted(result)


def filter_results():
    """Process get_results() output and filter them by gap.
    Return a list of tuple containing [(gap_value, results, time)]
    """

    results = get_results()
    final_list = []

    # gap_value counter
    for gap_value in range(1, 100):

        # common_digit counter
        for common_digit in range(0, 10):
            common = str(common_digit)
            step = gap_value
            common_list = []

            for count, result in enumerate(results):
                if step == count and common in result:
                    common_list.append(result)
                    step += (gap_value + 1)

            if common_list and len(common_list) >= 3:
                final_list.append((
                    gap_value, common, common_list))

    return final_list


def export_file(entry):

    gap, common, results = entry

    with open("results_solid_pattern_v1.1.txt", "a") as fo:
        fo.write("gap: {}\n".format(gap))
        fo.write("common: {}\n".format(common))
        fo.write("results: {}\n".format(results))
        fo.write("pairs:\n")
        for result in results:
            fo.write("{} <- {}\n".format(
                result, get_pairs(result, common)))
        fo.write("\n")


def main():
    with open("results_solid_pattern_v1.1.txt", "w") as fo:
        fo.write("")

    for entry in filter_results():
        gap, common, results = entry

        export_file(entry)

        print("gap: {}".format(gap))
        print("common: {}".format(common))
        print("results: {}".format(results))
        print("pairs:")
        for result in results:
            print("{} <- {}".format(result, get_pairs(result, common)))
        print("\n")


if __name__ == "__main__":
    main()
