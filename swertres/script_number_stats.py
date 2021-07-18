from re import split


def main():
    u_input = input("Enter weekly results (sun - sat): ")
    su_input = split(r"\s{1,}", u_input.strip())

    t_digits = 0

    t_even = 0
    t_odd = 0

    t_high = 0
    t_low = 0

    t_high_even = 0
    t_high_odd = 0

    t_low_even = 0
    t_low_odd = 0

    t_pos_1_even = 0
    t_pos_2_even = 0
    t_pos_3_even = 0

    t_pos_1_odd = 0
    t_pos_2_odd = 0
    t_pos_3_odd = 0

    for res in su_input:
        for pos, d in enumerate(res, 1):
            d = int(d)

            if pos == 1:
                if d % 2 == 0:
                    t_pos_1_even += 1
                else:
                    t_pos_1_odd += 1
            elif pos == 2:
                if d % 2 == 0:
                    t_pos_2_even += 1
                else:
                    t_pos_2_odd += 1
            else:
                if d % 2 == 0:
                    t_pos_3_even += 1
                else:
                    t_pos_3_odd += 1

            if d in [1, 2, 3, 4, 5]:
                t_low += 1

                if d % 2 == 0:
                    t_even += 1
                    t_low_even += 1

                else:
                    t_odd += 1
                    t_low_odd += 1

            else:
                t_high += 1

                if d % 2 == 0:
                    t_even += 1
                    t_high_even += 1

                else:
                    t_odd += 1
                    t_high_odd += 1

            t_digits += 1

    print(f'total digits: {t_digits}')
    print('\n')
    print(f'even: {t_even} - {t_even / t_digits * 100:.2f}')
    print(f'odd: {t_odd} - {t_odd / t_digits * 100:.2f}')
    print('\n')
    print(f'high: {t_high} - {t_high / t_digits * 100:.2f}')
    print(f'low: {t_low} - {t_low / t_digits * 100:.2f}')
    print('\n')
    print(f'high_odd: {t_high_odd} - {t_high_odd / t_digits * 100:.2f}')
    print(f'high_even: {t_high_even} - {t_high_even / t_digits * 100:.2f}')
    print('\n')
    print(f'low_odd: {t_low_odd} - {t_low_odd / t_digits * 100:.2f}')
    print(f'low_even: {t_low_even} - {t_low_even / t_digits * 100:.2f}')
    print('\n')
    print(f'pos_1_even: {t_pos_1_even} - {t_pos_1_even / t_digits * 100:.2f}')
    print(f'pos_2_even: {t_pos_2_even} - {t_pos_2_even / t_digits * 100:.2f}')
    print(f'pos_3_even: {t_pos_3_even} - {t_pos_3_even / t_digits * 100:.2f}')
    print('\n')
    print(f'pos_1_odd: {t_pos_1_odd} - {t_pos_1_odd / t_digits * 100:.2f}')
    print(f'pos_2_odd: {t_pos_2_odd} - {t_pos_2_odd / t_digits * 100:.2f}')
    print(f'pos_3_odd: {t_pos_3_odd} - {t_pos_3_odd / t_digits * 100:.2f}')


if __name__ == "__main__":
    main()
