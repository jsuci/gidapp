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

What this script will do is:
1. search through all the list of results
2. filter only results that has a common digit and length of 3
3. after filtering check the pairs of each result. check if:
    a. first(prev), second(prev), third(curr) pairs are in sequence
    ex.
        [(20), 90]
        [(30), 80]
        [(40), 80]

    b. first and second pairs are the same
    ex.
        [20, 90]
        [30, (80)]
        [40, (80)]

    c. first and third pairs are the same
    ex.
        [05, (35)]
        [75, 77]
        [33, (35)]

"""

from itertools import *


def get_results():
    """Get all the previous result and store it in reverse order"""

    results = []
    with open("results_v1.txt", "r") as fi:
        for line in islice(fi, 2, None):
            results.insert(0, line.strip())

    return results


def get_pairs(digit):
    """Given any digit return pairs of that digit"""
    result = []

    for pair in combinations(digit, 2):
        pair = "".join(pair)
        result.append(pair)

    return result


def filter_results():
    # Load all results

    # Check each result if it has a common digit
    # until no common digit is found. After that increment
    # 1 to the gap

    results = get_results()
    final_list = []

    for gap_value in range(1, len(results)):
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


def pair_seq(results, common):
    """Given a list of result check if it is in sequence or not 
    return True else False
    """
    pass


def main():
    for entry in filter_results():
        gap, common, results = entry
        print("gap: {}".format(gap))
        print("common: {}".format(common))
        print("results: {}".format(results))
        print("pairs:")
        for result in results:
            print("{} <- {}".format(result, get_pairs(result)))
        print("\n")


if __name__ == "__main__":
    main()
