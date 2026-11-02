from pathlib import Path
import pandas as pd
import json

CACHE_DIR = Path(__file__).parent / "cache"

def make_key(ticker: str, period: str, interval: str):
    key = ticker + "__" + period + "__" + interval
    return key

def load_cache(key: str):
    path = CACHE_DIR / (key + ".parquet")
    df = pd.read_parquet(path)
    return df

def save_cache(key:str, df: pd.DataFrame):
    path = CACHE_DIR / (key + ".parquet")
    df.to_parquet(path)
