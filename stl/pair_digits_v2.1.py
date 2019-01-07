import re
from itertools import islice, combinations

def is_sequence(digits):

    count = 0
    start = int(digits[0])
    for e in digits:
        e = int(e)

        if (e - start) == 1:
            count += 1
            if count == 2:
                return True
        else:
            count = 0

        start = e

    return False


def get_common_digit(results):
    count = 0
    for i in range(10):
        for e in results:
            if str(i) in e:
                count += 1
            else:
                count = 0

        if count == 3:
            return i

def get_sequence(common, results):
    output_pair = set()
    output_digit = set()
    digit = str(common)

    for e in results:
        for x in combinations(e, 2):
            if digit in x:
                output_digit.add("".join(x).replace(digit, "", 1))
                output_pair.add("".join(sorted(x)))

    sorted_pair = sorted(output_pair)
    sorted_digit = sorted(output_digit)

    if is_sequence(sorted_digit):
        if len(sorted_digit) == 6:
            first_half = is_sequence(sorted_digit[:3])
            second_half = is_sequence(sorted_digit[3:])
            
            if first_half and second_half:
                return (sorted_pair, sorted_digit, True)
            else:
                return (sorted_pair, sorted_digit, False)
        else:
            return (sorted_pair, sorted_digit, False)
    else:
        return (None, None, None)



def get_output(to_skip):
    for outer_count in range(2, 20):
        with open("results_v2.txt", "r") as f2:
            step = outer_count + to_skip
            num_match = 0
            time_results = {"11am": [], "4pm": [], "9pm": []}

            for count, line in enumerate(
                list(islice(f2, 2, None))[::-1]):
                date_digits = re.split(r"\s{10}", line.strip())

                if count == step and num_match != 3:
                    for i, e in enumerate(date_digits[1:]):
                        if i == 0:
                            time_results["11am"].append(e)
                        elif i == 1:
                            time_results["4pm"].append(e)
                        else:
                            time_results["9pm"].append(e)

                    num_match += 1
                    step += (outer_count + 1)

            for k, v in time_results.items():
                common_digit = get_common_digit(v)

                if common_digit:
                    seq_pair, seq_digit, total_seq = get_sequence(common_digit, v)
                    
                    if seq_digit:
                        if total_seq:
                            print("result_gap: {}\ntime: {}\ncommon_digit: {}\nis_seq: {}\nprev_results: {}\nseq_digit: {}\n\n".format(outer_count, k, common_digit, total_seq, v, seq_digit))
                        else:
                            print("result_gap: {}\ntime: {}\ncommon_digit: {}\nis_seq: {}\nprev_results: {}\nseq_digit: {}\n\n".format(outer_count, k, common_digit, total_seq, v, seq_digit))



def main():
    with open("results_v2.txt", "r") as f1:
        curr_results = f1.readline().strip().split()[-1]
        to_skip = 0

        if curr_results != "2":
            to_skip = 1

        get_output(to_skip)

            

if __name__ == "__main__":
    main()