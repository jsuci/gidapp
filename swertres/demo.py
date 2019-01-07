# import re
# from itertools import islice, combinations


# def main():
#     outer_count = 8
#     with open("results_v2.txt", "r") as f1:
#         split_date = f1.readline().strip().split(" ")
#         curr_results = split_date[-1]
#         curr_date = " ".join(split_date[1:len(split_date) - 1])

#         if curr_results != "2":
#             print("Results are not ready yet. [{}]".format(curr_date))
#         else:
#             step = outer_count
#             num_match = 0

#             time_results = {"11am": [], "4pm": [], "9pm": []}

#             for count, line in enumerate(list(islice(f1, 2, None))[::-1]):
#                 date_digits = re.split(r"\s{10}", line.strip())

#                 if count == step and num_match != 3:
#                     print(date_digits, "*")

#                     num_match += 1
#                     step += (outer_count + 1)
#                 else:
#                     print(date_digits)


# if __name__ == "__main__":
#     main()


output = set()

if output:
    print(True)
else:
    print(False)