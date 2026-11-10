import pandas as pd

def returns(close:  pd.Series) -> pd.Series:
    return close.pct_change().dropna().rename("return")

def buy_and_hold(close: pd.Series, cash: float, fee: float = 0.0, start: str | None = None) -> pd.Series:
    close = close.loc[start:]
    return ((cash - fee) * close / close.iloc[0].rename("buy_and_hold"))

def drawdown(equity: pd.Series) -> pd.Series:
    return (equity / equity.cummax() - 1).rename("drawdown")

def summary(equity: pd.Series, cash: float) -> dict[str, float]:
    growth = equity.iloc[-1] / cash
    years = (equity.index[-1] - equity.index[0].days / 365.25)
    bar_returns = returns(equity)
    bars_per_year = len(bar_returns) / years
    return {
        "total return": growth - 1,
        "yearly_return": growth ** (1 / years) - 1,
        "yearly_volatility": bar_returns.std() * bars_per_year ** 0.5,
        "max_drawdown": drawdown(equity).min(),
    }