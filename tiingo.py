import os
import requests
import pandas as pd

key = os.environ["TIINGO_API_KEY"]
headers = {"Authorization": f"Token {key}"}

def fetch_from_tiingo(ticker: str, start: str, end: str, interval: str) -> pd.DataFrame:
    frequency_map = {
        "1m": "1min", "5m": "5min", "15m": "15min", "30m": "30min",
        "1h": "60min", "60min": "60min"
    }
    clean_interval = frequency_map.get(interval.lower(), interval)

    params = {"startDate": start, 
          "endDate": end, 
          "resampleFreq": clean_interval,
          "columns": "date,open,high,low,close,volume"
          }
    
    try:
        result = pd.DataFrame(requests.get(f"https://api.tiingo.com/iex/{ticker.strip().upper()}/prices", params=params, headers=headers, timeout=10).json()).set_index("date")
        result.index = pd.to_datetime(result.index, utc=True)

        if result is None:
            print(f"No data returned: {ticker} historical data")
            return None
            
        if isinstance(result, pd.DataFrame) and result.empty:
            print(f"Empty dataframe returned: {ticker} historical data")
            return None
            
        print(f"Sucessfully retrieved: {ticker} historical data")
        return result
    except Exception as e:
        print(f"Failed to retrieve {ticker} historical data: {e}")
        return None