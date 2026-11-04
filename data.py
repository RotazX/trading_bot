from cache import make_key, load_cache, save_cache, is_fresh
from config import MAX_AGE_DAILY, MAX_AGE_INTRADAY
from yahoo import fetch_from_yahoo
from tiingo import fetch_from_tiingo
import pandas as pd

def get_data(ticker: str, start: str, end: str, interval: str) -> tuple[pd.DataFrame, str]:
    key = make_key(ticker, start, end, interval)

    is_intraday = interval.endswith(("m", "h"))
    max_age = MAX_AGE_INTRADAY if is_intraday else MAX_AGE_DAILY

    if is_fresh(key, max_age):
        return load_cache(key), "cache"

    df = fetch_from_yahoo(ticker, start, end, interval)

    if df is None:
        df = fetch_from_tiingo(ticker, start, end, interval)
        if df is None:
            raise RuntimeError(f"No data available for {ticker}")
        return df, "tiingo API"

    save_cache(key, df)
    return df, "yahoo API"