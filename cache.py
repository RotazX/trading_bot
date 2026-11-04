from pathlib import Path
import pandas as pd
from datetime import datetime, timezone

CACHE_DIR = Path(__file__).parent / "cache"

def make_key(ticker: str, start: str, end: str, interval: str) -> str:
    return f"{ticker.upper()}__{start}-{end}__{interval}"

def _path(key: str) -> Path:
    return CACHE_DIR / f"{key}.parquet"

def is_fresh(key: str, max_age) -> bool:
    path = _path(key)
    if not path.exists():
        return False
    modified = datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)
    return datetime.now(timezone.utc) - modified < max_age

def load_cache(key: str) -> pd.DataFrame:
    return pd.read_parquet(_path(key))

def save_cache(key:str, df: pd.DataFrame) -> None:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    df.to_parquet(_path(key))
