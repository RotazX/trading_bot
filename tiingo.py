import os
import requests
import pandas as pd

key = os.environ["TIINGO_API_KEY"]
url = "https://api.tiingo.com/tiingo/daily/AAPL/prices"
params = {"startDate": "2026-10-01", "endDate": "2026-11-01"}
headers = {"Authorization": f"Token {key}"}

def fetch_from_tiingo(ticker: str, period: str, interval: str) -> pd.DataFrame:
    r = requests.get(url, params=params, headers=headers, timeout=10).json()[:2]

    df = pd.DataFrame(r)
    return df, "tiingo API"

