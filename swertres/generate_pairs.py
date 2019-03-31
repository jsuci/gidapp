from datetime import *

def gen_pairs():
    pairs = []
    for first_d in range(0, 10):
        for second_d in range(first_d, 10):
            pairs.append("{}{}".format(first_d,
                second_d))

    return pairs


def gen_month():
    pass


print(gen_pairs())