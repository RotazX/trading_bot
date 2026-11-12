import pandas as pd
import pytest
from indicators import buy_and_hold, drawdown, fee_report, returns, summary, trade_fee

def prices(*values):
    index = pd.date_range("2024-01-01", periods=len(values), freq="D", tz="UTC")
    return pd.Series(values, index=index, dtype=float)

def test_returns_are_fractions_without_first_nan():
    assert returns(prices(100, 110, 99)).tolist() == pytest.approx([0.10, -0.10])

def test_trade_fee_uses_percentage_or_minimum():
    assert trade_fee(10_000, rate=0.001, minimum=1) == pytest.approx(10)
    assert trade_fee(500, rate=0.001, minimum=1) == pytest.approx(1)

def test_buy_and_hold_starts_at_cash_minus_fee():
    value = buy_and_hold(prices(100, 150, 50), cash=1000, fee_rate=0.001, min_fee=2)
    assert value.tolist() == pytest.approx([998, 1497, 499])

def test_buy_and_hold_start_date():
    value = buy_and_hold(prices(100, 200, 300), cash=1000, start="2024-01-02")
    assert value.tolist() == pytest.approx([1000, 1500])

def test_does_not_change_input():
    close = prices(100, 110)
    buy_and_hold(close, 1000)
    returns(close)
    assert close.tolist() == [100, 110]

def test_drawdown():
    assert drawdown(prices(100, 120, 90, 130)).tolist() == pytest.approx([0, 0, -0.25, 0])

def test_summary():
    equity = pd.Series([100.0, 200.0], index=pd.to_datetime(["2024-01-01", "2026-01-01"], utc=True))
    result = summary(equity, cash=100)
    assert result["total_return"] == pytest.approx(1.0)
    assert result["yearly_return"] == pytest.approx(2 ** (1 / 2.0007) - 1, rel=1e-3)

def test_summary_counts_fee():
    equity = buy_and_hold(prices(100, 100), cash=1000, fee_rate=0.001, min_fee=1)
    assert summary(equity, cash=1000)["total_return"] == pytest.approx(-0.001)