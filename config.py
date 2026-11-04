from datetime import timedelta

# freshness limits (daily vs intraday), retry count
MAX_AGE_INTRADAY = timedelta(minutes=15)
MAX_AGE_DAILY = timedelta(hours=12)

# What to analyse
TICKER = "TSLA"
START = "2025-01-01" 
END = "2026-01-01"
INTERVAL = "1h"

# Strategy
SHORT_WINDOW = 20      # short moving average (days)
LONG_WINDOW = 50       # long moving average (days)

# Money
STARTING_CASH = 1000.0   # euros
FEE_PER_TRADE = 1.0      # euros per buy or sell; check your broker's real fee
TAX_RATE = 0.22          # on realised profit; check the current Estonian rate