import yfinance as yf
import pandas as pd
from typing import Callable, Any

# s_data = yf.Ticker("AAPL")

def fetch_from_yahoo(ticker, start, end, interval) -> Any | None: # name: str, fetch: Callable[[], Any]
    try:
        result = yf.Ticker(ticker).history(start=start, end=end, interval=interval)[["Open", "High", "Low", "Close", "Volume"]] # fetch()

        if result is None:
            print(f"No data returned: {ticker} historical data")
            return None
        
        if isinstance(result, pd.DataFrame) and result.empty:
            print(f"Empty dataframe returned: {ticker} historical data")
            return None

        result.index = pd.to_datetime(result.index, utc=True)
        result = result.rename_axis('date')
        result.columns = result.columns.str.lower()
        
        print(f"Sucessfully retrieved: {ticker} historical data")
        return result
    except Exception as e:
        print(f"Failed to retrieve {ticker} historical data: {e}")
        return None