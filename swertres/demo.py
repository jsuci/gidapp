from itertools import permutations, combinations

# a = {'11am': ['15', '16', '17'], '4pm': ['15', '14', '13'], '9pm': ['11', '16', '11']}


# def is_descend(sum_list):
#     init_value = int(sum_list[0])
#     true_count = 0

#     for e in sum_list:
#         e = int(e)
#         if e == init_value:
#             true_count += 1
#         init_value -= 1

#     if true_count == 3:
#         return True
#     else:
#         return False

# def is_ascend(sum_list):
#     init_value = int(sum_list[0])
#     true_count = 0

#     for e in sum_list:
#         e = int(e)
#         if e == init_value:
#             true_count += 1
#         init_value += 1

#     if true_count == 3:
#         return True
#     else:
#         return False


# for k, v in a.items():
#     if is_descend(v):
#         print(k, v)

#     if is_ascend(v):
#         print(k, v)

def sum_all(digits):
    return sum([int(x) for x in digits])


a = combinations(range(10), 3)
possible_combi = []
for e in a:
    if sum_all(e) == 12:
        possible_combi.append("".join([str(x) for x in e]))
print(", ".join(possible_combi))