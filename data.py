from cache import make_key, load_cache, save_cache
from yahoo import fetch_from_yahoo
import pandas as pd

def get_data(ticker, period, interval):
    source = ""
    key = make_key(ticker, period, interval)
    print(key)

    df = load_cache(key)

    if isinstance(df, pd.DataFrame) and df.empty:
        return df, "cache"
    else:
        df = fetch_from_yahoo(ticker, period, interval)
        save_cache(key, df)
        return df, "yahoo API"

get_data("AAPL", "5d", "1h")
