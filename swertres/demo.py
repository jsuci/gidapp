# import requests
# import fileinput
# import time
# from bs4 import BeautifulSoup as BS
# from itertools import islice


# def fetch_html(mo, yr):
#     headers = {
#         "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3163.100 Safari/537.36"
#     }

#     year_month_url = "https://www.gidapp.com/lottery/philippines/pcso/suertres/month/{}-{}".format(
#         yr, mo)

#     r = requests.get(year_month_url, headers=headers)

#     print(r.content, r.status_code)


# def convert_month(data):
#     return {
#         "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5,
#         "jun": 6, "jul": 7, "aug": 8, "sep": 9, "oct": 10,
#         "nov": 11, "dec": 12
#     }[data]


# def get_results(file_month, file_date, file_year):
#     """Fetch results from given file_month, file_date and file_year
#     and returns a list of (output, index, status_code)
#     """

#     # A list of tuples: [(date, [results],...)]
#     output = []
#     status_code = ""
#     index = ""
#     end_date = ""

#     content, status_code = fetch_html(file_month, file_year)
#     soup = BS(content, "html.parser")
#     entries = soup.find_all("div", class_="result")

#     for i, e in enumerate(entries):
#         web_date_list = e.h4.time.get_text().split(" ")
#         web_date = "{:02} {} {} {}".format(
#             int(web_date_list[1]),
#             web_date_list[0][:3].lower(),
#             web_date_list[2][:3].lower(),
#             web_date_list[3].lower()
#         )
#         web_results = [y.get_text() for y in e.select(
#             "tbody > tr > td > span") if y.get_text() != "-"]
#         web_date_results_time = (web_date, web_results, len(
#             web_results) - 1)

#         if web_date == file_date:
#             index = i
#         else:
#             index = 0

#         output.append(web_date_results_time)

#         end_date = output[-1][0]

#     print(output, end_date, index, status_code)


# def export_results(output, index, file_date, file_time):
#     """Given the output(collected date, results, time), index(
#     skip one entry ahead), file_date(for comparison on the web_date),
#     file_time(for comparison with the current time results). Return
#     the new date and time
#     """

#     with open("results_v2.txt", "a") as fi:
#         for date_results_time in islice(output, index, None):
#             date, results, time = date_results_time

#             """Check if entries in file are identical to the ones
#             on the web. If they are then skip and process the next
#             entry.
#             """
#             if date == file_date and time == file_time:
#                 continue
#             else:
#                 if date == file_date:
#                     new_line_count = 0
#                     digit_index = file_time + 1

#                     for digits in islice(results, digit_index, None):
#                         print(digits)
#                         fi.write("{:>13}".format(digits))
#                         new_line_count += 1

#                     # Decide when add new line inside file
#                     if new_line_count == 2 or digit_index == 2:
#                         fi.write("\n")

#                 else:
#                     fi.write(date)

#                     new_line_count = 0
#                     for digits in results:
#                         print(digits)
#                         fi.write("{:>13}".format(digits))
#                         new_line_count += 1

#                     if new_line_count == 3:
#                         fi.write("\n")

#     print(date, time)


# def update_file_date_time(new_date, new_time):
#     updated_date_time = "updated: {} {}".format(
#         new_date, new_time)

#     with fileinput.input("results_v2.txt", inplace=True) as fio:
#         for entry in fio:
#             if ":" in entry:
#                 print(updated_date_time)
#             else:
#                 print(entry, end="")


# def main():
#     with open("results_v2.txt", "r") as fi:
#         file_date_list = fi.readline().strip().split()
#         file_date = " ".join(file_date_list[1:5])
#         file_month = convert_month(file_date_list[3])
#         file_year = int(file_date_list[4])
#         file_time = int(file_date_list[5])

#     while True:
#         curr_date = file_date

#         output, curr_date, index, status_code = get_results(
#             file_month, curr_date, file_year)

#         if status_code != 404:

#             new_date, new_time = export_results(
#                 output, index, file_date, file_time)

#             update_file_date_time(new_date, new_time)

#             if file_month == 12:
#                 file_month = 1
#                 file_year = file_year + 1
#             else:
#                 file_month += 1

#             time.sleep(5)
#         else:
#             break

#     print("Results are now up to date.")


# if __name__ == "__main__":
#     main()

############################################

# from timeit import *
# from itertools import *
# import re


# def get_last_result():
#     """Get the last result and return a string of digit"""
#     with open("results_v2.txt") as fi:
#         last_result = list(fi)[-1].split(" ")[-1].strip()

#         return last_result


# def get_last_two_results():
#     """Get the last result and return a list of digit"""
#     with open("results_v2.txt") as fi:
#         entries = [re.split(r"\s{10}", e.strip()) for e in fi]
#         last_result = []

#         if len(entries[-1]) == 4:
#             last_result.extend(entries[-2][1:])
#             last_result.extend(entries[-1][1:])
#         else:
#             last_result.extend(entries[-3][1:])
#             last_result.extend(entries[-2][1:])

#         return last_result


# def get_combinations(digits):
#     combi = []

#     for permute in permutations(digits, 3):

#         # # Limit permutations
#         # if digits[0] == permute[0]:
#         #     combi.append("".join(permute))

#         # Generate all possible permutations
#         combi.append("".join(permute))

#     return combi


# def compare_digits(digit_one, digit_two):
#     compare_count = 0

#     for j in set(digit_one):
#         if j in set(digit_two):
#             compare_count += 1

#     # Set to >= 2 for is_pair() and == 3 for has_common()
#     if compare_count == 3:
#         return True
#     else:
#         return False


# def search_results(digits, exact_loc=0):
#     with open("results_v2.txt", "r") as fi:
#         entries = [re.split(r"\s{10}", e.strip()) for e in fi]
#         index = 0

#         while index < (len(entries) - 1):

#             if digits in entries[index]:

#                 # Get the position of the focus digit
#                 curr_res_loc = entries[index].index(digits)

#                 prev_res = entries[index - 1]
#                 curr_res = entries[index]
#                 next_res = entries[index + 1]
#                 accu_entries = (prev_res, curr_res, next_res)

#                 filtered_res = exact_location(
#                     accu_entries, curr_res_loc, exact_loc)
#                 # filtered_res = is_pair(accu_entries, curr_res_loc)
#                 # filtered_res = has_common(accu_entries, curr_res_loc)

#                 if filtered_res:
#                     for e in filtered_res:
#                         print(e)

#                     print("\n")

#             index += 1


# def is_pair(accu_res, digit_loc):
#     """Given accu_res(tuple consisting prev, curr, nxt results)
#     and digit_loc(index in which the given digit was found) check
#     if the top digit and bottom digit has at least 2 same digits.
#     Return filtered results.
#     """

#     prev, curr, nxt = accu_res
#     is_pair_count = False

#     # compare_digits() controls the number of
#     # successful comparisons
#     if len(nxt) != 3 and compare_digits(
#             prev[digit_loc], nxt[digit_loc]):
#         is_pair_count = True

#     if is_pair_count:
#         return accu_res


# def has_common(accu_res, digit_loc):
#     """Filter accu_res using the last two lines of the current
#     results. If the last_tow_results contains at least 2 digits
#     in accu_res then return that accu_res
#     """

#     prev, curr, nxt = accu_res
#     chain_res = [e for e in chain(prev[1:], curr[1:], nxt[1:])]
#     res_to_compare = get_last_two_results()
#     compare_count = 0

#     for digit_one in res_to_compare:
#         for digit_two in chain_res:
#             if compare_digits(digit_one, digit_two):
#                 compare_count += 1

#     if compare_count == 2:
#         return accu_res


# def no_filter(accu_res, digit_loc):
#     return accu_res


# def exact_location(accu_res, digit_loc, exact_loc):
#     if digit_loc == exact_loc:
#         return has_common(accu_res, digit_loc)


# def main():
#     for digits in get_combinations('150'):
#         search_results(digits, exact_loc=3)


# if __name__ == "__main__":
#     main()

####################################################

# from timeit import *
# from itertools import *
# import re


# def get_combinations(digits):
#     combi = []

#     for permute in permutations(digits, 3):

#         # Generate all possible permutations
#         combi.append("".join(permute))

#     return combi


# def get_accu_results(result):
#     all_res = []
#     for digits in get_combinations(result):
#         with open("results_v2.txt", "r") as fi:
#             entries = [re.split(r"\s{10}", e.strip()) for e in fi]
#             index = 0

#             while index < (len(entries) - 1):

#                 if digits in entries[index]:

#                     # Get the position of digits
#                     curr_res_loc = entries[index].index(digits)
#                     prev_res = entries[index - 1]
#                     curr_res = entries[index]
#                     next_res = entries[index + 1]
#                     accu_entries = (prev_res, curr_res, next_res, curr_res_loc)

#                     all_res.append(accu_entries)

#                 index += 1

#     return all_res


# def is_total_match(digit_one, digit_two):
#     compare_count = 0

#     for j in set(digit_one):
#         if j in set(digit_two):
#             compare_count += 1

#     # for j in digit_one:
#     #     if j in digit_two:
#     #         compare_count += 1

#     # Set to >= 2 for is_pair() and == 3 for has_common()
#     if compare_count == 3:
#         return True
#     else:
#         return False


# def search_results(accu_one, accu_two):
#     """accu_one contains all the accumulated results
#     from different permutations of a given result.
#     accu_two is a list of permutations from a given
#     number. This script will filter out accu_one results
#     using accu_two combinations and returns a list of tuple
#     containing (prev, curr, nxt, loc)
#     """

#     results = []

#     for prev_curr_nxt_loc in accu_one:
#         prev, curr, nxt, loc = prev_curr_nxt_loc

#         for comp_digit in accu_two:
#             if (is_total_match(prev[loc], comp_digit) and
#                     prev_curr_nxt_loc not in results):
#                 results.append(prev_curr_nxt_loc)

#     return results


# def main():
#     # Compare it to this digit
#     accu_two = get_combinations("480")

#     # Get all results
#     accu_one = get_accu_results("507")

#     for result in search_results(accu_one, accu_two):
#         prev, curr, nxt, loc = result
#         print("{}\n{} {}\n{}\n\n".format(prev, curr, loc, nxt))


# if __name__ == "__main__":
#     main()

#############################################################

# import re
# from itertools import *


# def get_gap_results(match_count):
#     final_accu_res = []

#     for gap_value in range(1, 20):
#         with open("results_v2.txt", "r") as fi:

#             # Turn to list and reverse it
#             entries = [re.split(r"\s{2,}", e.strip())
#                        for e in fi][::-1]

#             # Control the number of matches
#             num_matches = 0

#             # Add one to step_count if results are not finished yet
#             to_skip = 0 if len(entries[0]) == 4 else 1
#             step_count = gap_value + to_skip

#             temp_accu_res = {"11am": [], "4pm": [], "9pm": []}

#             for count, entry in enumerate(entries):
#                 if (count == step_count and
#                         num_matches != match_count):

#                     temp_accu_res["11am"].append(entry[1])
#                     temp_accu_res["4pm"].append(entry[2])
#                     temp_accu_res["9pm"].append(entry[3])

#                     step_count += gap_value + 1
#                     num_matches += 1

#             final_accu_res.append((gap_value, temp_accu_res))

#     return final_accu_res


# def get_seq_type(list_of_digits):
#     """Given a list of unsorted integers ex. [4, 8, 3, ...] from
#     0 to 9 of any given length, check if all the values fit the
#     conditions below:
#         if all digits has a difference of 1 then return 1
#         if some digits are in sequence and the other digit has
#         a difference of of 2 then return 2
#         else return 0
#     """
#     list_of_digits = [int(e) for e in list_of_digits]
#     list_of_digits.sort()
#     start = list_of_digits[0]
#     first_digit = list_of_digits[0]
#     last_digit = list_of_digits[-1]
#     diff_not_one = []

#     for digit in islice(list_of_digits, 1, None):
#         if abs(start - digit) != 1:
#             diff_not_one.append(abs(start - digit))

#         start = digit

#     diff_not_one.sort()

#     len_diff_not_one = len(diff_not_one)

#     if not len_diff_not_one:
#         return 1
#     else:
#         if first_digit == 0 and last_digit == 9:
#             if len_diff_not_one == 1:
#                 if diff_not_one[0] == 2:
#                     return 2
#                 else:
#                     return 1
#             elif (
#                 len_diff_not_one == 2 and
#                 diff_not_one[0] == 2 and
#                 diff_not_one[1] != 2
#             ):
#                 return 2
#             else:
#                 return 0
#         elif first_digit == 0 and last_digit == 8:
#             if len_diff_not_one == 1:
#                 return 2
#             else:
#                 return 0
#         else:
#             if len_diff_not_one == 1 and diff_not_one[0] == 2:
#                 return 2
#             else:
#                 return 0


# def get_all_results():
#     all_results = []
#     for match_count in range(3, 9):
#         for entry in get_gap_results(match_count):
#             all_results.append(entry)

#     return all_results


# def get_next_digit(list_of_digits):
#     """Given a list of string digits ('1', '2', '3') or ['1', '2', 3]
#     get their start and end digits and then subtract or add to get the
#     next digit. Returns a list of subtracted and added values
#     """

#     list_of_digits = [int(e) for e in list_of_digits]
#     list_of_digits.sort()
#     start = list_of_digits[0]
#     end = list_of_digits[-1]

#     results = [str(0) if end + 1 == 10 else str(end + 1),
#                str(9) if start - 1 == -1 else str(start - 1)]

#     return sorted(results)


# def get_in_between_digit(list_of_digits):
#     """Given a list of string digits ('5', '3') or ['6', '8']
#     get their start and end digits and if there difference is
#     2 then get their in between value
#     """

#     list_of_digits = [int(e) for e in list_of_digits]
#     list_of_digits.sort()

#     start = list_of_digits[0]
#     first = list_of_digits[0]
#     end = list_of_digits[-1]

#     for digit in islice(list_of_digits, 1, None):

#         if (digit - start) == 2:
#             return str(start + 1)

#         # 0 and 8 has a gap of 2 and
#         # 1 and 9 has a gap of 2
#         elif (first == 0) and (end == 8):
#             return str(9)
#         elif (first == 1) and (end == 9):
#             return str(0)
#         else:
#             start = digit


# def get_position(result_collection):
#     """Given a list of tuple containing an int(gap_value)
#     and dictionary of results {"11am": ['123', ...]}
#     classify the possible digits and formulate new possible
#     pairs
#     """
#     eleven_am = {"first": set(), "second": set(), "third": set()}
#     four_pm = {"first": set(), "second": set(), "third": set()}
#     nine_pm = {"first": set(), "second": set(), "third": set()}

#     final_pair_results = {"11am": [], "4pm": [], "9pm": []}

#     for entry in result_collection:
#         gap_value, results = entry

#         for time, list_res in results.items():
#             if mark_positions(list_res):
#                 index, marked_res, poss_val = mark_positions(
#                     list_res)

#                 if time == "11am":
#                     if index[0] == 1:
#                         eleven_am["first"].add(poss_val[0])

#                     if index[0] == 2:
#                         eleven_am["second"].add(poss_val[0])

#                     if index[0] == 3:
#                         eleven_am["third"].add(poss_val[0])

#                 elif time == "4pm":
#                     if index[0] == 1:
#                         four_pm["first"].add(poss_val[0])

#                     if index[0] == 2:
#                         four_pm["second"].add(poss_val[0])

#                     if index[0] == 3:
#                         four_pm["third"].add(poss_val[0])

#                 else:
#                     if index[0] == 1:
#                         nine_pm["first"].add(poss_val[0])

#                     if index[0] == 2:
#                         nine_pm["second"].add(poss_val[0])

#                     if index[0] == 3:
#                         nine_pm["third"].add(poss_val[0])

#     # 11am
#     for pair_combi in product(eleven_am["first"],
#                               eleven_am["second"], eleven_am["third"]):
#         pair_combi_format = "".join(pair_combi)
#         final_pair_results["11am"].append(pair_combi_format)

#     for pair_combi in product(four_pm["first"],
#                               four_pm["second"], four_pm["third"]):
#         pair_combi_format = "".join(pair_combi)
#         final_pair_results["4pm"].append(pair_combi_format)

#     for pair_combi in product(nine_pm["first"],
#                               nine_pm["second"], nine_pm["third"]):
#         pair_combi_format = "".join(pair_combi)
#         final_pair_results["9pm"].append(pair_combi_format)

#     # 11am
#     for pair_combi in product(eleven_am["first"], eleven_am["second"]):
#         pair_combi_format = "{}{}-".format(
#             pair_combi[0], pair_combi[1])
#         final_pair_results["11am"].append(pair_combi_format)

#     for pair_combi in product(eleven_am["first"], eleven_am["third"]):
#         pair_combi_format = "{}-{}".format(
#             pair_combi[0], pair_combi[1])
#         final_pair_results["11am"].append(pair_combi_format)

#     for pair_combi in product(eleven_am["second"], eleven_am["third"]):
#         pair_combi_format = "-{}{}".format(
#             pair_combi[0], pair_combi[1])
#         final_pair_results["11am"].append(pair_combi_format)

#     # 4pm
#     for pair_combi in product(four_pm["first"], four_pm["second"]):
#         pair_combi_format = "{}{}-".format(
#             pair_combi[0], pair_combi[1])
#         final_pair_results["4pm"].append(pair_combi_format)

#     for pair_combi in product(four_pm["first"], four_pm["third"]):
#         pair_combi_format = "{}-{}".format(
#             pair_combi[0], pair_combi[1])
#         final_pair_results["4pm"].append(pair_combi_format)

#     for pair_combi in product(four_pm["second"], four_pm["third"]):
#         pair_combi_format = "-{}{}".format(
#             pair_combi[0], pair_combi[1])
#         final_pair_results["4pm"].append(pair_combi_format)

#     # 9pm
#     for pair_combi in product(nine_pm["first"], nine_pm["second"]):
#         pair_combi_format = "{}{}-".format(
#             pair_combi[0], pair_combi[1])
#         final_pair_results["4pm"].append(pair_combi_format)

#     for pair_combi in product(nine_pm["first"], nine_pm["third"]):
#         pair_combi_format = "{}-{}".format(
#             pair_combi[0], pair_combi[1])
#         final_pair_results["4pm"].append(pair_combi_format)

#     for pair_combi in product(nine_pm["second"], nine_pm["third"]):
#         pair_combi_format = "-{}{}".format(
#             pair_combi[0], pair_combi[1])
#         final_pair_results["9pm"].append(pair_combi_format)

#     return final_pair_results


# def mark_positions(list_results):
#     """Given a list of results ["234", "456", "789", ...]
#     identify which position has sequence and mark them with
#     "()" accordingly. Return a tuple containing the number
#     of identified positions, [1] if its location is 1 and if
#     there are two in a digit then return a list of positions
#     [1, 3], a list of marked_results ['3 0 (5)', ...] and
#     possible digit [6]
#     """

#     first_pos = []
#     second_pos = []
#     third_pos = []

#     for result in list_results:
#         first_pos.append(result[0])
#         second_pos.append(result[1])
#         third_pos.append(result[2])

#     first_seq = get_seq_type(first_pos)
#     second_seq = get_seq_type(second_pos)
#     third_seq = get_seq_type(third_pos)

#     first_pos_digit = get_in_between_digit(first_pos)
#     second_pos_digit = get_in_between_digit(second_pos)
#     third_pos_digit = get_in_between_digit(third_pos)

#     # Set first_seq, second_seq, third_seq to 1 if you want
#     # to filter results with gap of 1. If not then set it to 2
#     if (first_seq == 2) and (second_seq == 2) and (third_seq == 2):
#         all_format = ["({}) ({}) ({})".format(
#             x[0], x[1], x[2]) for x in list_results]

#         return ([1, 2, 3], all_format,
#                 [first_pos_digit, second_pos_digit, third_pos_digit])

#     elif (first_seq == 2) and (third_seq == 2):
#         first_third_format = ["({}) {} ({})".format(
#             x[0], x[1], x[2]) for x in list_results]

#         return ([1, 3], first_third_format,
#                 [first_pos_digit, third_pos_digit])

#     elif (first_seq == 2) and (second_seq == 2):
#         first_second_format = ["({}) ({}) {}".format(
#             x[0], x[1], x[2]) for x in list_results]

#         return ([1, 2], first_second_format,
#                 [first_pos_digit, second_pos_digit])

#     elif first_seq == 2:
#         first_pos_format = ["({}) {} {}".format(
#             x[0], x[1], x[2]) for x in list_results]

#         return ([1], first_pos_format, [first_pos_digit])

#     elif second_seq == 2:
#         second_post_format = ["{} ({}) {}".format(
#             x[0], x[1], x[2]) for x in list_results]

#         return ([2], second_post_format, [second_pos_digit])

#     elif third_seq == 2:
#         third_post_format = ["{} {} ({})".format(
#             x[0], x[1], x[2]) for x in list_results]

#         return ([3], third_post_format, [third_pos_digit])

#     else:
#         return None


# def main():
#     result_collection = get_all_results()
#     for key, values in get_position(result_collection).items():
#         print(key, values)


# if __name__ == "__main__":
#     main()

##########################################################
# """
# TODO: Fix the way the script determines if it is in_sequence
# or not. Separating the digits in to left and right digit is not
# the proper way since there are sequences that are left out
# ex.
#     [0, 5]
#     [3, 1]
#     [2, 6]
# The above sample when using left and right digit would turn out to
# be left = [0, 3, 2] which is not a diff_one sequence but there is a
# [0, 1, 2] and at the same time a diff_two sequence at [5, 3, 6] and
# [5, 3, 2]


# TODO: Change the way the script determine if it has a common_digit or
# not.
# """

# import re
# from itertools import *

# """
# Possible combinations produced using this script is good for
# 1 day use only. Use this script as guide for combinations
# produced using syn_digits_v2.1.py.
# """


# def get_gap_results():
#     """Gathers all gap results and returns a list of tuple
#     containing the gap_value and time, results dictionary
#     ex. [(2, {'11am': ['952', '517', '591'], '4pm': ['371',
#     '976', '433'], '9pm': ['019', '928', '653']})...]
#     """

#     gap_results_list = []

#     for gap_value in range(2, 100):
#         with open("results_v2.txt", "r") as fo:
#             last_entry = fo.readline().strip().split(" ")[-1]
#             reversed_entries = list(islice(fo, 1, None))[::-1]
#             to_skip = 0 if last_entry == "2" else 1
#             step_value = gap_value + to_skip
#             number_of_matches = 0
#             gap_results = {"11am": [], "4pm": [], "9pm": []}

#             for line_count, line_entry in enumerate(reversed_entries):
#                 date_results_list = re.split(r"\s{2,}", line_entry.strip())

#                 # Set number of matches here
#                 if line_count == step_value and number_of_matches != 3:
#                     gap_results["11am"].append(date_results_list[1])
#                     gap_results["4pm"].append(date_results_list[2])
#                     gap_results["9pm"].append(date_results_list[3])

#                     number_of_matches += 1
#                     step_value += gap_value + 1

#             gap_results_list.append((gap_value, gap_results))

#     return gap_results_list


# def get_next_digit(list_of_digits):
#     """Given a list of string digits ('1', '2', '3') or ['1', '2', 3]
#     get their start and end digits and then subtract or add to get the
#     next digit. Returns a list of subtracted and added values
#     """

#     list_of_digits = [int(e) for e in list_of_digits]
#     list_of_digits.sort()
#     start = list_of_digits[0]
#     end = list_of_digits[-1]

#     results = [str(0) if end + 1 == 10 else str(end + 1),
#                str(9) if start - 1 == -1 else str(start - 1)]

#     return sorted(results)


# def get_in_between_digit(list_of_digits):
#     """Given a list of string digits ('5', '3') or ['6', '8']
#     get their start and end digits and if there difference is
#     2 then get their in between value
#     """

#     list_of_digits = [int(e) for e in list_of_digits]
#     list_of_digits.sort()

#     start = list_of_digits[0]
#     first = list_of_digits[0]
#     end = list_of_digits[-1]
#     for digit in islice(list_of_digits, 1, None):

#         if (digit - start) == 2:
#             return str(start + 1)
#         elif (first == 0) and (end == 8):
#             return str(9)
#         elif (first == 1) and (end == 9):
#             return str(0)
#         else:
#             start = digit


# def is_sequence(list_of_digits):
#     """Given a list of unsorted string digits ex. ['4', '8'..]
#     from 0 to 9 of any given length, check if all the values fit the
#     conditions below:
#         if all digits has a difference of 1 then return 1
#         if some digits are in sequence and the other digit has
#         a difference of of 2 then return 2
#         else return 0
#     """
#     list_of_digits = [int(e) for e in list_of_digits]
#     list_of_digits.sort()
#     start = list_of_digits[0]
#     first_digit = list_of_digits[0]
#     last_digit = list_of_digits[-1]
#     diff_not_one = []

#     for digit in islice(list_of_digits, 1, None):
#         if abs(start - digit) != 1:
#             diff_not_one.append(abs(start - digit))

#         start = digit

#     diff_not_one.sort()

#     len_diff_not_one = len(diff_not_one)

#     if not len_diff_not_one:
#         return 1
#     else:
#         if first_digit == 0 and last_digit == 9:
#             if len_diff_not_one == 1:
#                 if diff_not_one[0] == 2:
#                     return 2
#                 else:
#                     return 1
#             elif (
#                 len_diff_not_one == 2 and
#                 diff_not_one[0] == 2 and
#                 diff_not_one[1] != 2
#             ):
#                 return 2
#             else:
#                 return 0
#         elif first_digit == 0 and last_digit == 8:
#             if len_diff_not_one == 1:
#                 return 2
#             else:
#                 return 0
#         else:
#             if len_diff_not_one == 1 and diff_not_one[0] == 2:
#                 return 2
#             else:
#                 return 0


# def has_common_digit(results):
#     """Given a result check if it has a common_digit. Return a list
#     of common digit.
#     """
#     common_digits = []

#     for seq in product(*results):
#         g = groupby(seq)
#         if next(g, True) and not next(g, False):
#             if seq[0] not in common_digits:
#                 common_digits.append(seq[0])

#     return common_digits


# def possible_digits(results, common):
#     seq = []
#     diff_one = []
#     diff_two = []
#     possible = []
#     status = ""

#     # Strip common digits to get pairs
#     for result in results:
#         temp = result
#         for digit in common:
#             temp = temp.replace(digit, "", 1)
#         seq.append(temp)

#     # Classify pairs into diff_one or diff_two
#     for digits in product(*seq):
#         if is_sequence(digits) == 1:
#             diff_one_digits = get_next_digit(digits)

#             if diff_one_digits not in diff_one:
#                 diff_one.append(diff_one_digits)
#         elif is_sequence(digits) == 2:
#             diff_two_digits = get_in_between_digit(digits)

#             if diff_two_digits not in diff_two:
#                 diff_two.append(diff_two_digits)
#         else:
#             pass

#     # Filter options
#     if len(common) == 2 and (diff_one or diff_two):
#         status = "two_common"
#         diff_one_two = diff_one if diff_one else diff_two
#         for combi in product(*common, *diff_one_two):
#             combi = "".join(combi)
#             possible.append(combi)

#     if len(common) == 1:
#         if diff_one and diff_two:
#             status = "diff_one_and_two"
#             for combi in product(common, chain(*diff_one), diff_two):
#                 combi = "".join(combi)
#                 possible.append(combi)

#         # elif diff_one:
#         #     status = "diff_one_only"
#         #     for combi in product(common, *diff_one):
#         #         combi = "".join(combi)
#         #         possible.append(combi)

#         elif diff_two and len(diff_two) == 2:
#             status = "diff_two_only"
#             diff_two_pairs = ["".join(e) for e in combinations(
#                 diff_two, 2)]
#             for combi in product(common, diff_two_pairs):
#                 combi = "".join(combi)
#                 possible.append(combi)
#         else:
#             pass

#     diffs = (diff_one, diff_two)

#     return (possible, status, diffs)


# def format_results(results, common):
#     final_output = []

#     for result in results:
#         for digit in result:
#             format_result = [
#                 "({})".format(e) if e in common else
#                 " {} ".format(e) for e in result
#             ]

#         final_output.append("".join(format_result))

#     return final_output


# def is_sync(results):
#     """Given a list of results ex. ['358', '468', '827', ...]
#     check if is in sync or not. By sync means it has:
#         a. common_digit
#         b. other digits must be in sequence (1, 2, 3.. or 3, 2, 1..)

#     If all conditions are satisfied then output the following:
#         a. common_digit
#         b. format_res
#         c. combis

#     ex. [3, 4, 2] [5, 6, 7] [('38', '58'), ('48', '68'),
#     ('28', '78')] 8
#     """

#     common_digits = has_common_digit(results)

#     if common_digits:
#         """After you have identified results that has common
#         digits you can now further filter the results by choosing
#         wether the pairs is in sequence or has a gap of 2
#         """
#         combis, status, diffs = possible_digits(results, common_digits)

#         if status:
#             format_res = format_results(results, common_digits)
#             output = (common_digits, format_res, combis, status, diffs)

#             return output


# def main():
#     for item in get_gap_results():
#         gap_value, gap_results = item
#         for time, results in gap_results.items():
#             if is_sync(results):
#                 common, format_res, combi, status, diffs = is_sync(results)
#                 print("gap: {}".format(gap_value))
#                 print("time: {}".format(time))
#                 print("status: {}".format(status))
#                 print("diffs: {}".format(diffs))
#                 print("common: {}".format(common))
#                 print("combi: {}".format(combi))
#                 print("results: ")
#                 for entry in format_res:
#                     print(entry)

#                 print("\n")


# if __name__ == "__main__":
#     main()
#     # print(possible_digits(['730', '280', '049'], ['0']))
#     # a = [['0', '6']]
#     # b = ['3', '4']
#     # for seq in product(['0'], *a, b):
#     #     print(seq)
#     # a = [['1', '5'], ['3', '7']]
#     # b = ['5', '3']

#     # for seq in product(['8'], chain(*a), b):
#     #     print(seq)
######################################################

# from itertools import *

# """
# Given a sequence of string numbers ['8', '9', '0', '1'...] determine
# what type of sequence it has. Return a string of seq_type
#     diff_one - if all numbers has a difference of 1
#     diff_two - if all numbers has a difference of 2
#     diff_zero - if all numbers has the same digit

#     gap_one - all of the numbers has a difference of one except 1
#         ex. 8, 9, 0, 1, 3 (2 missing)
#             7, 9, 0, 1, 2 (8 missing)

# Test cases:
#     diff_one:
#         1234
#         890
#         901
#         789
#         90
#         89
#         8901
#         789012
#         90123
#         5621
# """


# def diff_one(digit):
#     return {
#         0: 1,
#         1: 2,
#         2: 3,
#         3: 4,
#         4: 5,
#         5: 6,
#         6: 7,
#         7: 8,
#         8: 9,
#         9: 0
#     }[digit]


# def diff_two(digit):
#     return {
#         0: 2,
#         1: 3,
#         2: 4,
#         3: 5,
#         4: 6,
#         5: 7,
#         6: 8,
#         7: 9,
#         8: 0,
#         9: 1
#     }[digit]


# def seq_type(digits):
#     """
#     Given a sequence of string numbers ['8', '9', '0', '1'...] determine
#     what type of sequence it has. Return a string of seq_type
#         diff_one - if all numbers has a difference of 1
#         diff_two - if all numbers has a difference of 2
#         diff_zero - if all numbers has the same digit

#         gap_one - all of the numbers has a difference of one except 1
#             ex. 8, 9, 0, 1, 3 (2 missing)
#                 7, 9, 0, 1, 2 (8 missing)
#     """

#     uniq_digits = set([int(e) for e in digits])
#     diff_one_count = 0
#     diff_two_count = 0
#     diff_none_count = 0

#     if len(uniq_digits) == 1:
#         print("diff_zero")
#     elif len(uniq_digits) != len(digits):
#         print("has_double")
#     else:
#         for digit in uniq_digits:

#             if diff_one(digit) in uniq_digits:
#                 diff_one_count += 1
#             elif diff_two(digit) in uniq_digits:
#                 diff_two_count += 1
#             else:
#                 diff_none_count += 1

#         print(diff_one_count, diff_two_count, diff_none_count)

#         # Filter diff_one
#         if diff_two_count == 0 and diff_none_count < 2:
#             print("diff_one")

#         # Filter diff_two
#         if (
#             diff_one_count == 0 and
#             diff_two_count >= 1 and
#             diff_none_count != 2
#         ):
#             print("diff_two")

#         # Filter gap_one
#         if (
#             diff_one_count != 0 and
#             diff_two_count == 1 and
#             diff_none_count != 2
#         ):
#             print("gap_one")


# if __name__ == "__main__":
#     seq_type('08')
###########################################

# import re
# from itertools import *

# """
# Using this script find patterns by collecting results by gap_value.
# Print out the gap_value, time, common_digit, results, seq_type
# """


# def get_gap_results(matches=2):
#     """Gathers all gap results and returns a list of tuple
#     containing the gap_value and time, results dictionary
#     ex. [(2, {'11am': ['952', '517', '591'], '4pm': ['371',
#     '976', '433'], '9pm': ['019', '928', '653']})...]
#     """

#     gap_results_list = []

#     for gap_value in range(2, 100):
#         with open("results_v2.txt", "r") as fo:
#             last_entry = fo.readline().strip().split(" ")[-1]
#             reversed_entries = list(islice(fo, 1, None))[::-1]
#             to_skip = 0 if last_entry == "2" else 1
#             step_value = gap_value + to_skip
#             number_of_matches = 0
#             gap_results = {"11am": [], "4pm": [], "9pm": []}

#             for line_count, line_entry in enumerate(reversed_entries):
#                 date_results_list = re.split(r"\s{2,}", line_entry.strip())

#                 # Set number of matches here
#                 if line_count == step_value and number_of_matches != matches:
#                     gap_results["11am"].append(date_results_list[1])
#                     gap_results["4pm"].append(date_results_list[2])
#                     gap_results["9pm"].append(date_results_list[3])

#                     number_of_matches += 1
#                     step_value += gap_value + 1

#             gap_results_list.append((gap_value, gap_results))

#     return gap_results_list


# def diff_one(digit):
#     return {
#         0: 1,
#         1: 2,
#         2: 3,
#         3: 4,
#         4: 5,
#         5: 6,
#         6: 7,
#         7: 8,
#         8: 9,
#         9: 0
#     }[digit]


# def diff_two(digit):
#     return {
#         0: 2,
#         1: 3,
#         2: 4,
#         3: 5,
#         4: 6,
#         5: 7,
#         6: 8,
#         7: 9,
#         8: 0,
#         9: 1
#     }[digit]


# def seq_type(digits):
#     """
#     Given a sequence of string numbers ['8', '9', '0', '1'...] determine
#     what type of sequence it has. Return a string of seq_type
#         diff_one - if all numbers has a difference of 1
#         diff_two - if all numbers has a difference of 2
#         diff_zero - if all numbers has the same digit

#         gap_one - all of the numbers has a difference of one except 1
#             ex. 8, 9, 0, 1, 3 (2 missing)
#                 7, 9, 0, 1, 2 (8 missing)
#     """

#     uniq_digits = set([int(e) for e in digits])
#     diff_one_count = 0
#     diff_two_count = 0
#     diff_none_count = 0

#     if len(uniq_digits) == 1:
#         return "diff_zero"
#     elif len(uniq_digits) != len(digits):
#         return "has_double"
#     else:
#         for digit in uniq_digits:

#             if diff_one(digit) in uniq_digits:
#                 diff_one_count += 1
#             elif diff_two(digit) in uniq_digits:
#                 diff_two_count += 1
#             else:
#                 diff_none_count += 1

#         # print(diff_one_count, diff_two_count, diff_none_count)

#         # Filter diff_one
#         if diff_two_count == 0 and diff_none_count < 2:
#             return "diff_one"

#         # Filter diff_two
#         if (
#             diff_one_count == 0 and
#             diff_two_count >= 1 and
#             diff_none_count != 2
#         ):
#             return "diff_two"

#         # Filter gap_one
#         if (
#             diff_one_count != 0 and
#             diff_two_count == 1 and
#             diff_none_count != 2
#         ):
#             return "gap_one"


# def get_seq_type(results, common):
#     """Given a list of results ['123', '345', '678'...] and a list of
#     common digits remove common digits from results and then determine
#     their sequence type. Return a list of tupple containing the
#     digits and seq_type [(('9', '9', '9'), 'diff_zero')...]
#     """

#     results = [e.replace(f, "", 1) for f in common for e in results]

#     output = []

#     for seq in product(*results):
#         output_item = (seq, seq_type(seq))
#         if seq_type(seq) and output_item not in output:
#             output.append(output_item)

#     return output


# def has_common_digit(results):
#     """Given a result check if it has a common_digit. Return a list
#     of common digit.
#     """
#     common_digits = []

#     for seq in product(*results):
#         g = groupby(seq)
#         if next(g, True) and not next(g, False):
#             if seq[0] not in common_digits:
#                 common_digits.append(seq[0])

#     return common_digits


# def export_file(gap, time, common, results, seq_results):

#     with open("results_sync_digits_v2.4.txt", "a") as fo:
#         fo.write("gap: {}\n".format(gap))
#         fo.write("time: {}\n".format(time))
#         fo.write("common: {}\n".format(common))
#         fo.write("results: {}\n".format(results))
#         for seq in seq_results:
#             sequence, label = seq
#             fo.write("{} <- {}\n".format(
#                 sequence, label))
#         fo.write("\n")


# def main():
#     with open("results_sync_digits_v2.4.txt", "w") as fo:
#         fo.write("")

#     for item in get_gap_results(3):
#         gap_value, gap_results = item

#         for time, results in gap_results.items():
#             common = has_common_digit(results)

#             if common and time == "4pm":
#                 seq_results = get_seq_type(results, common)

#                 print("gap: {}".format(gap_value))
#                 print("time: {}".format(time))
#                 print("common: {}".format(common))
#                 print("results: {}".format(results))
#                 print("seq_type: ")
#                 for seq in seq_results:
#                     seq_digits, label = seq
#                     print("{} <- {}".format(seq_digits, label))

#                 print("\n")


# if __name__ == "__main__":
    # # main()

###############################################
# from itertools import *

# """
# Using this script find patterns by collecting results by gap_value.
# Unlike V1.2 I have set limit to the number of matches to 3. V1.2
# collects all results that has common until it is exhausted
# Print out the gap_value, time, common_digits, results, seq_type
# """


# def get_gap_results(matches=3):
#     """Gathers all gap results and returns a list of tuple
#     containing the gap_value and list of results ex.
#     [(2, ['952', '517', '591']),...]
#     """

#     gap_results_list = []

#     for gap_value in range(1, 200):
#         with open("results_v1.txt", "r") as fi:
#             reversed_entries = [
#                 e.strip() for e in islice(fi, 2, None)][::-1]
#             number_of_matches = 0

#             # Use as comparison for line_count
#             # while gap_value sets the gap
#             step_value = gap_value
#             results = []

#             for line_count, line_entry in enumerate(reversed_entries):

#                 # Set number of matches here
#                 if line_count == step_value and number_of_matches != matches:

#                     results.append(line_entry)

#                     number_of_matches += 1
#                     step_value += gap_value + 1

#             gap_results_list.append((gap_value, results))

#     return gap_results_list


# def diff_one(digit):
#     return {
#         0: 1,
#         1: 2,
#         2: 3,
#         3: 4,
#         4: 5,
#         5: 6,
#         6: 7,
#         7: 8,
#         8: 9,
#         9: 0
#     }[digit]


# def diff_two(digit):
#     return {
#         0: 2,
#         1: 3,
#         2: 4,
#         3: 5,
#         4: 6,
#         5: 7,
#         6: 8,
#         7: 9,
#         8: 0,
#         9: 1
#     }[digit]


# def seq_type(digits):
#     """
#     Given a sequence of string numbers ['8', '9', '0', '1'...] determine
#     what type of sequence it has. Return a string of seq_type
#         diff_one - if all numbers has a difference of 1
#         diff_two - if all numbers has a difference of 2
#         diff_zero - if all numbers has the same digit

#         gap_one - all of the numbers has a difference of one except 1
#             ex. 8, 9, 0, 1, 3 (2 missing)
#                 7, 9, 0, 1, 2 (8 missing)
#     """

#     uniq_digits = set([int(e) for e in digits])
#     diff_one_count = 0
#     diff_two_count = 0
#     diff_none_count = 0

#     if len(uniq_digits) == 1:
#         return "diff_zero"
#     elif len(uniq_digits) != len(digits):
#         return "has_double"
#     else:
#         for digit in uniq_digits:

#             if diff_one(digit) in uniq_digits:
#                 diff_one_count += 1
#             elif diff_two(digit) in uniq_digits:
#                 diff_two_count += 1
#             else:
#                 diff_none_count += 1

#         # print(diff_one_count, diff_two_count, diff_none_count)

#         # Filter diff_one
#         if diff_two_count == 0 and diff_none_count < 2:
#             return "diff_one"

#         # Filter diff_two
#         if (
#             diff_one_count == 0 and
#             diff_two_count >= 1 and
#             diff_none_count != 2
#         ):
#             return "diff_two"

#         # Filter gap_one
#         if (
#             diff_one_count != 0 and
#             diff_two_count == 1 and
#             diff_none_count != 2
#         ):
#             return "gap_one"


# def get_seq_type(results, common=[]):
#     """Given a list of results ['123', '345', '678'...] and a list of
#     common digits (optional). Remove common digits from results and
#     then determine their sequence type. Return a list of tuple
#     containing the digits and seq_type [(('9', '9', '9'),
#     'diff_zero')...]
#     """

#     trim_results = []

#     if common:
#         for result in results:
#             for c in common:
#                 result = result.replace(c, "", 1)
#             trim_results.append(result)
#     else:
#         trim_results = results

#     output = []

#     for seq in product(*trim_results):
#         output_item = (seq, seq_type(seq))
#         if seq_type(seq) and output_item not in output:
#             output.append(output_item)

#     return output


# def has_common_digit(results):
#     """Given a result check if it has a common_digit. Return a list
#     of common digit.
#     """
#     common_digits = []

#     for seq in product(*results):
#         g = groupby(seq)
#         if next(g, True) and not next(g, False):
#             if seq[0] not in common_digits:
#                 common_digits.append(seq[0])

#     return common_digits


# def filter_results():
#     """Process get_results() output and filter them by gap.
#     Return a list of tuple containing [(gap_value, common, results)]
#     """

#     results = get_results()
#     final_list = []

#     for gap_value in range(1, 200):
#         for common_digit in range(0, 10):
#             common = str(common_digit)
#             step = gap_value
#             common_list = []

#             for count, result in enumerate(results):
#                 if step == count and common in result:
#                     common_list.append(result)
#                     step += (gap_value + 1)

#             if common_list and len(common_list) >= 3:
#                 seq_types = get_seq_types(common_list, common)
#                 final_list.append((
#                     gap_value, common, common_list, seq_types))

#     return final_list


# def export_file(entry):

#     gap, common, results, seq_types = entry

#     with open("results_solid_pattern_v1.2.txt", "a") as fo:
#         fo.write("gap: {}\n".format(gap))
#         fo.write("common: {}\n".format(common))
#         fo.write("results: {}\n".format(results))
#         fo.write("pairs:\n")
#         for seq in seq_types:
#             sequence, label = seq
#             fo.write("{} <- {}\n".format(
#                 sequence, label))
#         fo.write("\n")


# def main():
#     for entry in get_gap_results():
#         gap_value, results = entry
#         common_digits = has_common_digit(results)

#         print(results, common_digits)
#         for seq in get_seq_type(results):
#             print(seq)
#         print("\n")


# if __name__ == "__main__":
#     main()


########################################################
# from itertools import *
# import re
# """
# Classify results by (month, year, [results]) and after that
# compare current month, year, results to all classified results
# count the number of results that
# """


# def classify_results():
#     """Process results_v2.txt and classify them according to month, year and
#     result. Return a list of tuple
#     """

#     final_result = []

#     with open("results_v2.txt", "r") as fi:

#         curr_month = ""
#         curr_month_results = []

#         for entry in islice(fi, 2, None):
#             entry = re.split(r"\s{2,}", entry.strip())
#             month = " ".join(entry[0].split(" ")[2:])
#             results = entry[1:]

#             if curr_month == month:
#                 curr_month_results.extend(results)
#             else:
#                 curr_month_results = []
#                 curr_month = month

#             to_append = (curr_month, curr_month_results)
#             if to_append not in final_result:
#                 final_result.append(to_append)

#     return final_result


# def compare_digits(digit_1, digit_2):

#     for num_1 in digit_1:
#         if num_1 in digit_2:
#             digit_2 = digit_2.replace(num_1, "", 1)

#     if len(digit_2) == 0:
#         return True
#     else:
#         return False


# def count_similar(results_1, results_2):
#     """Given a list of results_1 (['123', '456'...]) and
#     results_2 (['456', '789', ...]) count the number of
#     similarities. Return the number of similarities
#     """

#     count = 0

#     for digit_1 in results_1:
#         for digit_2 in results_2:
#             if compare_digits(digit_1, digit_2):
#                 count += 1

#     return (count, results_1)


# def filtered_results():
#     base_results = classify_results()
#     results_2 = base_results.pop(-1)[1]
#     highest = []
#     curr_highest = 0

#     for entry in base_results:
#         date, results_1 = entry
#         count, mark_results = count_similar(results_1, results_2)

#         if curr_highest < count:
#             curr_highest = count
#             highest = (date, count, mark_results)

#     return highest


# def main():
#     print(filtered_results())


# if __name__ == "__main__":
#     main()
############################################

# from itertools import *
# import re

# """
# Process results_v2.txt and look for digits that match
# the current result and position
# """

# def compare_digits(digit_1, digit_2):

#     for num_1 in digit_1:
#         if num_1 in digit_2:
#             digit_2 = digit_2.replace(num_1, "", 1)

#     if len(digit_2) == 0:
#         return True
#     else:
#         return False


# def filter_results(curr_result, time):

#     accu_result = []

#     with open("results_v2.txt", "r") as fi:
#         for entry in islice(fi, 2, None):
#             entry = re.split(r"\s{2,}", entry.strip())
#             date = entry[0]
#             results = entry[1:]

#             for count, result in enumerate(results):
#                 if (
#                     compare_digits(curr_result, result) and
#                     count == time
#                 ):
#                     accu_result.append((date, count, results))

#     return accu_result


# def main():
#     # The current result
#     curr_res = "971"

#     # Time, 0 for 11am, 1 for 4pm and 2 for 9pm
#     time = 0

#     for entry in filter_results(curr_res, time):
#         print(entry)




# if __name__ == "__main__":
#     main()

##########################################################
