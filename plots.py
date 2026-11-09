import matplotlib.pyplot as plt
import numpy as np
from indicators import daily_returns
from data import get_data
import config

def plot_returns_hist(returns, ticker):
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.hist(returns.dropna(), bins=100)
    ax.set_title(f"{ticker} daily returns")
    ax.set_xlabel("Daily return")
    ax.set_ylabel("Number of days")
    plt.show()

def plot_returns_linear(returns, ticker):
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(returns.dropna())
    ax.set_title(f"{ticker} daily returns")
    ax.set_xlabel("Daily return")
    ax.set_ylabel("Number of days")
    plt.show()

df, source = get_data(config.TICKER, config.START, config.END, config.INTERVAL) 

print(daily_returns(df))
plot_returns_hist(daily_returns(df), "NVDA")
plot_returns_linear(daily_returns(df), "NVDA")