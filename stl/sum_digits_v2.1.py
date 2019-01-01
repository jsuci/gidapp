from itertools import islice, combinations, permutations
from pathlib import Path
import re

def sum_all(digits):
    return sum([int(x) for x in digits])

def is_descend(sum_list):
    init_value = int(sum_list[0])
    last_value = int(sum_list[-1])
    true_count = 0

    for e in sum_list:
        e = int(e)
        if e == init_value:
            true_count += 1
        init_value -= 1

    if true_count == 3:
        return last_value - 1
    else:
        return False

def is_ascend(sum_list):
    init_value = int(sum_list[0])
    last_value = int(sum_list[-1])
    true_count = 0

    for e in sum_list:
        e = int(e)
        if e == init_value:
            true_count += 1
        init_value += 1

    if true_count == 3:
        return last_value + 1
    else:
        return False

def possible_combi(value):
    a = combinations(range(10), 3)
    possible_combi = []

    for e in a:
        if sum_all(e) == 12:
            possible_combi.append("".join([str(x) for x in e]))

    # return possible_combi
    return ", ".join(possible_combi)


def main():
    for outer_count in range(2, 30):
        with open("results_v2.txt") as fo:
            step = outer_count
            num_match_steps = 0
            digit_sum_tup = []
            digit_time_dic = {"11am": [], "4pm": [], "9pm": []}


            for i, e in enumerate(list(islice(fo, 2, None))[::-1]):
                digits =  re.split(r"\s{10}", e.strip())
                per_line = ["{:20}".format(digits[0])]

                """
                Skip the first n of results base on the value of step
                and then start counting ahead of step (step + outside 
                counter + 1) and limit the number of matches to 3 only
                """
                if i == step and num_match_steps != 3:
                    for digit in digits[1:]:
                        """
                        Construct a list tuple containing digit and
                        sum ex. [('609', '15')]
                        """
                        digit_sum_tup.append((digit, sum_all(digit)))

                    num_match_steps += 1
                    step += (outer_count + 1)

            """
            digit_sum_tup is a list of tuple containing a digit 
            and sum ex. [('609', '15')]
            """
            count_dic = 0
            for e in digit_sum_tup:
                e = e[1]
                if count_dic == 0:
                    digit_time_dic["11am"].append(e)
                    count_dic = 1
                elif count_dic == 1:
                    digit_time_dic["4pm"].append(e)
                    count_dic = 2
                else:
                    digit_time_dic["9pm"].append(e)
                    count_dic = 0

            """
            digit_time_dic is dictionary containing the time and 
            sum ex. {'11am': ['15', '16', '17']}
            """
            for k, v in digit_time_dic.items():
                value_down = is_descend(v)
                value_up = is_ascend(v)
                if value_down:
                    print("result_gap: {2}\ntime: {0}\nsum: {1}\npossible combi for {3}:\n{4}\n\n".format(
                        k, v, outer_count, value_down, possible_combi(value_down)))

                if value_up:
                    print("result_gap: {2}\ntime: {0}\nsum: {1}\npossible combi for {3}:\n{4}\n\n".format(
                        k, v, outer_count, value_down, possible_combi(value_down)))



if __name__ == "__main__":
    main()