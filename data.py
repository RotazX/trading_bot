import yfinance as yf
import pandas as pd
from typing import Callable, Any

s_data = yf.Ticker("AAPL")
US = yf.Market("US")

def safe_fetch(name: str, fetch: Callable[[], Any]) -> Any | None:  
    try:
        result = fetch()

        if result is None:
            print(f"No data returned: {name}")
            return None
        
        if isinstance(result, pd.DataFrame) and result.empty:
            print(f"Empty dataframe returned: {name}")
            return None
        
        print(f"Sucessfully retrieved: {name}")
        return result
    except Exception as e:
        print(f"Failed to retrieve {name}: {e}")
        return None

def load_data():
    test = [
        safe_fetch("stock info", lambda: s_data.info),
        # safe_fetch("calandar", lambda: s_data.calendar),
        # safe_fetch("analyst price targets", lambda: s_data.analyst_price_targets),
        # safe_fetch("quarterly income statement", lambda: s_data.quarterly_income_stmt),
        # safe_fetch("historical prices", lambda: s_data.history(period='1mo')),
        # safe_fetch("option calls", lambda: s_data.option_chain(s_data.options[0]).calls)
    ]

    # status = safe_fetch("US market status", lambda: US.status)
    # summary = safe_fetch("US market summary", lambda: US.summary)

    return test # status, summary