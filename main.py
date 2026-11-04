import config
import data as d
import pandas as pd

def main() -> None:
    df, source = d.get_data(config.TICKER, config.START, config.END, config.INTERVAL) 
    pd.set_option("display.precision", 3)

    print(f"Data is from {source}:")
    print(df)

    # for v in test:
    #     print(v)
    #     print()

if __name__ == "__main__":
    main()