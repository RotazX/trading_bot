import config
import data as d

def main() -> None:
    df, source = d.get_data(config.TICKER, config.PERIOD, config.INTERVAL) 

    print(f"Data is from {source}:")
    print(df)

    # for v in test:
    #     print(v)
    #     print()

if __name__ == "__main__":
    main()