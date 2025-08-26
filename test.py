import yfinance as yf
import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor
import matplotlib.dates  # Added this import for num2date

# List of top 10 cryptocurrencies and approximate circulating supply (in millions, based on 2025 estimates)
tickers = ["BTC-USD", "ETH-USD", "BNB-USD", "SOL-USD", "XRP-USD", "ADA-USD", "AVAX-USD", "DOGE-USD", "MATIC-USD", "DOT-USD"]
circulating_supply = {
    "BTC": 19.7,    # ~19.7M BTC
    "ETH": 120.2,   # ~120.2M ETH
    "BNB": 166.8,   # ~166.8M BNB
    "SOL": 466.0,   # ~466M SOL
    "XRP": 56.7,    # ~56.7B XRP
    "ADA": 36.0,    # ~36B ADA
    "AVAX": 394.2,  # ~394.2M AVAX
    "DOGE": 146.0,  # ~146B DOGE
    "MATIC": 9.9,   # ~9.9B MATIC
    "DOT": 1.4      # ~1.4B DOT
}

# Fetch data for all tickers
data = {}
for ticker in tickers:
    coin = ticker.split('-')[0]
    df = yf.download(ticker, start="2024-01-01", end="2025-08-26", progress=False)
    if not df.empty:
        df['Market Cap'] = df['Close'] * (circulating_supply[coin] * 1000000 if coin != "XRP" else circulating_supply[coin] * 1000000000)
        data[coin] = df

# Plot all market caps with cursor
fig, ax = plt.subplots(figsize=(12, 8))
for coin, df in data.items():
    ax.plot(df.index, df['Market Cap'] / 1e12, label=coin, linewidth=1.5)

ax.set_title('Top 10 Cryptocurrencies Historical Market Cap (Trillions USD)', fontsize=14)
ax.set_xlabel('Date', fontsize=12)
ax.set_ylabel('Market Cap (Trillions USD)', fontsize=12)
ax.grid(True)
ax.legend()

# Add cursor to show market cap under mouse
cursor = Cursor(ax, useblit=True, color='red', linewidth=1)
def on_move(event):
    if event.inaxes:
        x, y = event.xdata, event.ydata
        if x is not None and y is not None:
            ax.format_coord = lambda x, y: f'Date: {matplotlib.dates.num2date(x).strftime("%Y-%m-%d")}, Market Cap: {y:.2f}T USD'

# Connect the mouse move event
fig.canvas.mpl_connect('motion_notify_event', on_move)

plt.tight_layout()
plt.show()