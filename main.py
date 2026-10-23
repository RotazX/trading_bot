import data as d

def main() -> None:
    test = d.load_data() # , status, summary
    # print(f"US market status:\n {status}")
    # print(f"US market summary:\n {summary}")

    # print("-----------------------------------")

    for v in test:
        print(v)
        print()


if __name__ == "__main__":
    main()