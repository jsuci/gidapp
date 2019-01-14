# from itertools import islice


# def is_sequence(list_of_digits):
#     list_of_digits.sort()
#     start = list_of_digits[0]
#     first_digit = list_of_digits[0]
#     last_digit = list_of_digits[-1]
#     diff_not_one = []

#     print(list_of_digits)

#     for digit in islice(list_of_digits, 1, None):
#         print(start, digit, abs(start - digit))
#         if abs(start - digit) != 1:
#             diff_not_one.append(abs(start - digit))

#         start = digit

#     diff_not_one.sort()
#     len_diff_not_one = len(diff_not_one)


#     print(diff_not_one)

#     if not len_diff_not_one:
#         print(1)
#     else:
#         if first_digit == 0 and last_digit == 9:
#             if len_diff_not_one == 1:
#                 print(1)
#             elif len_diff_not_one == 2 and diff_not_one[0] == 2:
#                 print(2)
#             else:
#                 print(0)
#         elif first_digit == 0 and last_digit == 8:
#             if len_diff_not_one == 1:
#                 print(2)
#             else:
#                 print(0)
#         else:
#             if len_diff_not_one == 1 and diff_not_one[0] == 2:
#                 print(2)

# is_sequence([1, 2, 3, 6, 0, 8, 9])

from itertools import islice


def is_sequence(list_of_digits):
    list_of_digits.sort()
    start = list_of_digits[0]
    first_digit = list_of_digits[0]
    last_digit = list_of_digits[-1]
    diff_not_one = []

    print(list_of_digits)

    for digit in islice(list_of_digits, 1, None):
        print(start, digit, abs(start - digit))
        if abs(start - digit) != 1:
            diff_not_one.append(abs(start - digit))

        start = digit

    diff_not_one.sort()
    len_diff_not_one = len(diff_not_one)

    print(diff_not_one)

    if not len_diff_not_one:
        print(1)
    else:
        if first_digit == 0 and last_digit == 9:
            if len_diff_not_one == 1:
                print(1)
            elif len_diff_not_one == 2 and diff_not_one[0] == 2:
                print(2)
            else:
                print(0)
        elif first_digit == 0 and last_digit == 8:
            if len_diff_not_one == 1:
                print(2)
            else:
                print(0)
        else:
            if len_diff_not_one == 1 and diff_not_one[0] == 2:
                print(2)


is_sequence([1, 2, 3, 6, 0, 8, 9])
