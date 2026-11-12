import matplotlib.pyplot as plt
import config
from data import get_data
from indicators import buy_and_hold, summary, fee_report
from plots import plot_report

def main() -> None:
    df, source = get_data(config.TICKER, config.START, config.END, config.INTERVAL) 
    print(f"Data is from {source}")

    equity = buy_and_hold(df["close"], config.STARTING_CASH, config.FEE_RATE, config.MIN_FEE)
    for name, value in summary(equity, config.STARTING_CASH).items():
        print(f"{name:>18}: {value:8.2%}")

    for name, value in fee_report(df["close"], config.STARTING_CASH, config.FEE_RATE, config.MIN_FEE).items():
        print(f"{name:>18}: {value:8.2f}€")

    print(f"Cash after holding: {equity.iloc[-1]:8.2f}")


    plot_report(df["close"], equity, config.TICKER, config.INTERVAL)
    plt.show()

if __name__ == "__main__":
    main()