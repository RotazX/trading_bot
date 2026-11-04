from cache import make_key, load_cache, save_cache, is_fresh
from config import MAX_AGE_DAILY, MAX_AGE_HISTORICAL, MAX_AGE_INTRADAY
from yahoo import fetch_from_yahoo
from tiingo import fetch_from_tiingo
import pandas as pd

COLUMNS = ["open", "high", "low", "close", "volume"]

def _is_intraday(interval: str) -> bool:
    return interval.endswith(("m", "h"))

def _max_age(end: str, interval: str):
    if pd.Timestamp(end, tz="UTC") < pd.Timestamp.now("UTC"):
        return MAX_AGE_HISTORICAL
    return MAX_AGE_INTRADAY if _is_intraday(interval) else MAX_AGE_DAILY

def _standardize(df: pd.DataFrame, interval: str) -> pd.DataFrame:
    if df.empty:
        raise ValueError("No rows returned")
    df = df[COLUMNS].astype(float)
    df.index = pd.to_datetime(df.index, utc=True).rename("date")
    if not _is_intraday(interval):
        df.index = df.index.normalize()
    return df

def get_data(ticker: str, start: str, end: str, interval: str) -> tuple[pd.DataFrame, str]:
    ticker = ticker.strip().upper()
    key = make_key(ticker, start, end, interval)

    if is_fresh(key, _max_age(end, interval)):
        df = load_cache(key)
        return df, f"cache ({df.attrs.get('source', 'unknown')})"

    for source, fetch in (("yahoo API", fetch_from_yahoo), ("tiingo API", fetch_from_tiingo)):
        try:
            df = _standardize(fetch(ticker, start, end, interval), interval)
        except Exception as e:
            print(f"{source} failed for {ticker}: {e}")
            continue
        df.attrs["source"] = source
        save_cache(key, df)
        return df, source   

    raise RuntimeError(f"No data available for {ticker}")