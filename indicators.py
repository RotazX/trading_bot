import pandas as pd
import config
from data import get_data

def daily_returns(prices: pd.DataFrame) -> pd.DataFrame:
    prices['NVDA_Pct_Change'] = prices["close"].pct_change() * 100
    return prices['NVDA_Pct_Change']

def buy_and_hold(prices: pd.DataFrame, time: str, size: int):
    rates = daily_returns(prices) / 100
    compund_growth = (rates + 1).cumprod()
    prices['buy_and_hold'] = size * compund_growth
    return prices['buy_and_hold']

df, source = get_data(config.TICKER, config.START, config.END, config.INTERVAL) 

print(buy_and_hold(df, "2025-02-10", 1000000))
    

