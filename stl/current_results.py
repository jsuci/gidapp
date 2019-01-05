
def main():
    with open("results_v2.txt", "r") as fo:
        for i, e in enumerate(list(fo)[::-1]):
            if i == 0:
                print(e.strip())



if __name__ == "__main__":
    main()