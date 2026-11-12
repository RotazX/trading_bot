import pandas as pd

def returns(close:  pd.Series) -> pd.Series:
    return close.pct_change().dropna().rename("return")

def trade_fee(amount: float, rate: float, minimum:float = 0.0) -> float:
    return max(minimum, amount * rate)  

def buy_and_hold(close: pd.Series, cash: float, fee_rate: float = 0.0, min_fee: float = 0.0, start: str | None = None) -> pd.Series:
    close = close.loc[start:]
    invested = cash - trade_fee(cash, fee_rate, min_fee)
    return (invested * close / close.iloc[0]).rename("buy_and_hold")

def drawdown(equity: pd.Series) -> pd.Series:
    return (equity / equity.cummax() - 1).rename("drawdown")

def summary(equity: pd.Series, cash: float) -> dict[str, float]:
    growth = equity.iloc[-1] / cash
    years = (equity.index[-1] - equity.index[0]).days / 365.25
    bar_returns = returns(equity)
    bars_per_year = len(bar_returns) / years
    return {
        "total_return": growth - 1,
        "yearly_return": growth ** (1 / years) - 1,
        "yearly_volatility": bar_returns.std() * bars_per_year ** 0.5,
        "max_drawdown": drawdown(equity).min(),
    }

def fee_report(close: pd.Series, cash: float, fee_rate: float, min_fee: float = 0.0, start: str | None = None) -> dict[str, float]:
    with_fees = buy_and_hold(close, cash, fee_rate, min_fee, start)
    without_fees = buy_and_hold(close, cash, start=start)
    buy_fee = trade_fee(cash, fee_rate, min_fee)
    sell_fee = trade_fee(with_fees.iloc[-1], fee_rate, min_fee)
    return {
        "buy_fee": buy_fee,
        "sell_fee": sell_fee,
        "fees_paid": buy_fee + sell_fee,
        "lost_to_fees": without_fees.iloc[-1] - (with_fees.iloc[-1] - sell_fee),
    }