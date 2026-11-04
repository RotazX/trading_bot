import yfinance as yf
import pandas as pd

def fetch_from_yahoo(ticker, start, end, interval) -> pd.DataFrame:
        df = yf.Ticker(ticker).history(start=start, end=end, interval=interval)
        return df.rename(columns=str.lower)