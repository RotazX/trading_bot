import pandas as pd

def daily_returns(prices: pd.DataFrame):
    prices['NVDA_Pct_Change'] = prices["close"].pct_change() * 100
    return prices['NVDA_Pct_Change']