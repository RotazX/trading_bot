import os
import pandas as pd
import pytest
import data
import cache

ARGS = ("AAPL", "2025-01-01", "2025-01-10", "1d")

def fake_prices(*_):
    dates = pd.date_range("2025-01-02", periods=3, freq="D", tz="America/New_York")
    return pd.DataFrame({"open": 1.0, "high": 2.0, "low": 0.5, "close": [100.0, 101.5, 99.8], "volume": 10}, index=dates)

def fail(*_):
    raise ConnectionError("down")

@pytest.fixture(autouse=True)
def temp_cache(tmp_path, monkeypatch):
    monkeypatch.setattr(cache, "CACHE_DIR", tmp_path)
    return tmp_path

def test_fetches_once_then_uses_cache(monkeypatch):
    calls = []
    monkeypatch.setattr(data, "fetch_from_yahoo", lambda *a: calls.append(a) or fake_prices())

    first, source1 = data.get_data(*ARGS)
    second, source2 = data.get_data(*ARGS)

    assert len(calls) == 1
    assert (source1, source2) == ("yahoo API", "cache (yahoo API)")
    pd.testing.assert_frame_equal(first, second, check_freq=False)

def test_falls_back_and_caches_backup(monkeypatch):
    monkeypatch.setattr(data, "fetch_from_yahoo", fail)
    monkeypatch.setattr(data, "fetch_from_tiingo", fake_prices)

    assert data.get_data(*ARGS)[1] == "tiingo API"
    assert data.get_data(*ARGS)[1] == "cache (tiingo API)"

def test_empty_result_triggers_fallback(monkeypatch):
    monkeypatch.setattr(data, "fetch_from_yahoo", lambda *a: pd.DataFrame())
    monkeypatch.setattr(data, "fetch_from_tiingo", fake_prices)

    assert data.get_data(*ARGS)[1] == "tiingo API"

def test_raises_when_all_sources_fail(monkeypatch):
    monkeypatch.setattr(data, "fetch_from_yahoo", fail)
    monkeypatch.setattr(data, "fetch_from_tiingo", fail)

    with pytest.raises(RuntimeError):
        data.get_data(*ARGS)

def test_refetches_stale_cache(temp_cache, monkeypatch):
    monkeypatch.setattr(data, "fetch_from_yahoo", fake_prices)
    data.get_data(*ARGS)
    for path in temp_cache.iterdir():
        os.utime(path, (0, 0))

    assert data.get_data(*ARGS)[1] == "yahoo API"

def test_daily_timestamps_are_standardized(monkeypatch):
    monkeypatch.setattr(data, "fetch_from_yahoo", fake_prices)
    df, _ = data.get_data(*ARGS)

    assert list(df.columns) == data.COLUMNS
    assert (df.index == df.index.normalize()).all()
    assert str(df.index.tz) == "UTC"