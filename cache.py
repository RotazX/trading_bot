from pathlib import Path
import pandas as pd
import json

base = Path(__file__).parent / "cache"

def make_key(ticker: str, period: str, interval: str):
    key = ticker + "__" + period + "__" + interval
    return key

def load_cache(key: str):
    path = base / (key + ".parquet")
    df = pd.read_parquet(path)
    return df

def save_cache(key:str, df: pd.DataFrame):
    path = base / (key + ".parquet")
    df.to_parquet(path) 
