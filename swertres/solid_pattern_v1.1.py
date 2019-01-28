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
    """Get all the previous result and store it in reverse order"""

    results = []
    with open("results_v1.txt", "r") as fi:
        for line in islice(fi, 2, None):
            results.insert(0, line.strip())

    return results


def filter_results():
    # Load all results

    # Check each result if it has a common digit
    # until no common digit is found. After that increment
    # 1 to the gap

    results = get_results()
    final_list = []

    for gap_value in range(1, len(results)):
        for common_digit in range(0, 10):
            step = gap_value
            common_list = []

            for count, result in enumerate(results):
                if step == count and str(common_digit) in result:
                    common_list.append(result)
                    step += (gap_value + 1)

            if common_list and len(common_list) >= 3:
                final_list.append((
                    gap_value, common_digit, common_list))

    return final_list


def main():
    for entry in filter_results():
        print(entry)


if __name__ == "__main__":
    main()
