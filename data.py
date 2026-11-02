from cache import make_key, load_cache, save_cache
from yahoo import fetch_from_yahoo
import pandas as pd

def get_data(ticker, period, interval):
    key = make_key(ticker, period, interval)

    try:
        df = load_cache(key)
    except Exception:
        df = pd.DataFrame()

    if isinstance(df, pd.DataFrame) and not df.empty:
        return df, "cache"
    else:
        df = fetch_from_yahoo(ticker, period, interval)
        if df is not None:
            save_cache(key, df)
        else:
            return None, "API"
        return df, "yahoo API"