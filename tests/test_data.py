import pandas as pd
import data
import cache

def fake_prices():
    dates = pd.date_range("2024-01-01", periods=3, freq="D")
    return pd.DataFrame({"Close": [100.0, 101.5, 99.8]}, index=dates)

def test_fetches_once_then_uses_cache(tmp_path, monkeypatch):
    monkeypatch.setattr(cache, "CACHE_DIR", tmp_path)

    calls = []

    def fake_fetch(ticker, period, interval):
        calls.append(ticker)
        return fake_prices()

    monkeypatch.setattr(data, "fetch_from_yahoo", fake_fetch)

    first, source1 = data.get_data("AAPL", "1y", "1d")
    assert len(calls) == 1
    assert source1 == "yahoo API"

    second, source2 = data.get_data("AAPL", "1y", "1d")
    assert len(calls) == 1
    assert source2 == "cache"

    pd.testing.assert_frame_equal(first, second, check_freq=False)