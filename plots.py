import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter, StrMethodFormatter 
from indicators import drawdown, returns

def plot_report(close, equity, ticker: str, interval: str) -> plt.Figure:
    fig, axes = plt.subplot_mosaic([["value", "value"], ["drawdown", "hist"]], figsize=(11, 7), layout="constrained")
    fig.suptitle(f"{ticker} buy and hold ({interval} bars)")

    axes["value"].plot(equity)
    axes["value"].set(title="Portfolio value", ylabel="Value (€)")
    axes["value"].yaxis.set_major_formatter(StrMethodFormatter("{x:,.0f}"))

    axes["drawdown"].fill_between(equity.index, drawdown(equity), color="tab:red", alpha=0.4)
    axes["drawdown"].set(title="Drawdown from peak", ylabel="Below peak")

    axes["hist"].hist(returns(close), bins=100)
    axes["hist"].set(title=f"Return per {interval} bar", xlabel="Return")

    axes["drawdown"].yaxis.set_major_formatter(PercentFormatter(1))
    axes["hist"].xaxis.set_major_formatter(PercentFormatter(1))
    for ax in axes.values():
        ax.grid(alpha=0.3)
    for name in ("value", "drawdown"):
        axes[name].xaxis.set_major_formatter(mdates.ConciseDateFormatter(axes[name].xaxis.get_major_locator()))
    return fig