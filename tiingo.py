import os
import requests
import pandas as pd

BASE_URL = "https://api.tiingo.com"
INTRADAY = {"1m": "1min", "5m": "5min", "15m": "15min", "30m": "30min", "60m": "60min", "1h": "60min"}
DAILY = {"1d": "daily", "1wk": "weekly", "1mo": "monthly"}
ADJUSTED = {"adjOpen": "open", "adjHigh": "high", "adjLow": "low", "adjClose": "close", "adjVolume": "volume"}

def fetch_from_tiingo(ticker: str, start: str, end: str, interval: str) -> pd.DataFrame:
    is_intraday = interval in INTRADAY
    path = f"iex/{ticker}/prices" if is_intraday else f"tiingo/daily/{ticker}/prices"
    params = {"startDate": start, "endDate": end, "resampleFreq": (INTRADAY if is_intraday else DAILY)[interval]}
    if is_intraday:
        params["columns"] = "open,high,low,close,volume"

    headers = {"Authorization": f"Token {os.environ["TIINGO_API_KEY"]}"}
    response = requests.get(f"{BASE_URL}/{path}", params=params, headers=headers, timeout=10)
    response.raise_for_status()

    df = pd.DataFrame(response.json())

    if df.empty:
        return df
    if not is_intraday:
        df = df[["date", *ADJUSTED]].rename(columns=ADJUSTED)
    df = df.set_index("date")
    df.index = pd.to_datetime(df.index, utc=True)
    return df[df.index < pd.Timestamp(end, tz="utc")] # So the end would be exclusive, like in Yahoo