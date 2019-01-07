from itertools import repeat, islice

def has_digit(outer_count, digits):
    if outer_count in digits:
        return True

def main():
    # for outer_count in range(10):
        outer_count = 5
        with open("results_v1.txt", "r") as fo:
            filtered_results = [x.strip() for x in islice(fo, 2, None) if str(outer_count) in x]
            print(filtered_results)


if __name__ == "__main__":
    main()