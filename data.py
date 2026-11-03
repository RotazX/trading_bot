from cache import make_key, load_cache, save_cache, is_fresh
from config import MAX_AGE_DAILY, MAX_AGE_INTRADAY
from yahoo import fetch_from_yahoo
import pandas as pd

def get_data(ticker, period, interval):
    key = make_key(ticker, period, interval)

    is_intraday = interval.endswith(("m", "h"))
    max_age = MAX_AGE_INTRADAY if is_intraday else MAX_AGE_DAILY

    if is_fresh(key, max_age):
        return load_cache(key), "cache"

    df = fetch_from_yahoo(ticker, period, interval)

    if df is None:
        raise RuntimeError(f"No data available for {ticker}")

    save_cache(key, df)
    return df, "yahoo API"