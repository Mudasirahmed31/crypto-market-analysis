"""
Cryptocurrency Market Analysis (2015-2021) — Exploratory Data Analysis
Coins: Bitcoin (BTC), Ethereum (ETH), Binance Coin (BNB), Dogecoin (DOGE)
Author: Mudasir Ahmed

Answers ten self-defined market questions and saves supporting charts to
analysis/images/, matching the metrics shown in the Power BI dashboard
(Cryptocurrency_Market_Analysis__2015-2021_.pbix).
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

plt.rcParams["figure.facecolor"] = "#160318"
plt.rcParams["axes.facecolor"] = "#160318"
plt.rcParams["savefig.facecolor"] = "#160318"
plt.rcParams["axes.edgecolor"] = "#888"
plt.rcParams["axes.labelcolor"] = "white"
plt.rcParams["text.color"] = "white"
plt.rcParams["xtick.color"] = "white"
plt.rcParams["ytick.color"] = "white"
plt.rcParams["grid.color"] = "#3a2340"

PINK = "#F72585"
CYAN = "#4CC9F0"
GOLD = "#F2A900"
GREEN = "#4ADE80"
COLORS = {"Bitcoin": PINK, "Ethereum": CYAN, "Binance Coin": GOLD, "Dogecoin": GREEN}

IMG = "images/"

files = {
    "Bitcoin": "../data/coin_Bitcoin.csv",
    "Ethereum": "../data/coin_Ethereum.csv",
    "Binance Coin": "../data/coin_BinanceCoin.csv",
    "Dogecoin": "../data/coin_Dogecoin.csv",
}

coins = {}
for name, path in files.items():
    d = pd.read_csv(path, parse_dates=["Date"])
    d = d.sort_values("Date").reset_index(drop=True)
    coins[name] = d

all_df = pd.concat(coins.values(), ignore_index=True)
print("Total rows across all coins:", len(all_df))
print("Date range:", all_df["Date"].min(), "to", all_df["Date"].max())

# ---------------------------------------------------------------------------
# Q1. How did each coin's closing price evolve over its full history?
# ---------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(9, 5))
for name, d in coins.items():
    ax.plot(d["Date"], d["Close"], label=name, color=COLORS[name], linewidth=1.2)
ax.set_yscale("log")
ax.set_title("Q1: Closing Price Over Time (log scale)", color="white")
ax.set_ylabel("Close Price (USD, log scale)")
ax.legend(facecolor="#160318", labelcolor="white")
plt.tight_layout()
plt.savefig(IMG + "q1_close_over_time.png", dpi=140)
plt.close()

# ---------------------------------------------------------------------------
# Q2. What is the all-time Max Rate and Min Rate for each coin? (dashboard cards)
# ---------------------------------------------------------------------------
print("\nQ2 - Max / Min Close price per coin:")
for name, d in coins.items():
    print(f"  {name}: max={d['Close'].max():.4f}  min={d['Close'].min():.8f}")

# ---------------------------------------------------------------------------
# Q3. What's the max % growth (low -> high) for each coin? (dashboard: 75,885,995K%)
# ---------------------------------------------------------------------------
print("\nQ3 - Max growth % (from all-time low Close to all-time high Close):")
growth = {}
for name, d in coins.items():
    lo, hi = d["Close"].min(), d["Close"].max()
    pct = (hi - lo) / lo * 100
    growth[name] = pct
    print(f"  {name}: {pct:,.0f}%  (low {lo:.8f} -> high {hi:,.2f})")

fig, ax = plt.subplots(figsize=(6, 4))
names = list(growth.keys())
vals = [growth[n] for n in names]
bars = ax.bar(names, vals, color=[COLORS[n] for n in names])
ax.set_yscale("log")
ax.set_title("Q3: Max Growth % (Low \u2192 High), log scale", color="white")
ax.set_ylabel("% Growth (log scale)")
plt.xticks(rotation=15)
plt.tight_layout()
plt.savefig(IMG + "q3_max_growth.png", dpi=140)
plt.close()

# ---------------------------------------------------------------------------
# Q4. How did trading volume evolve, and which coin dominates?
# ---------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(9, 5))
for name, d in coins.items():
    ax.plot(d["Date"], d["Volume"], label=name, color=COLORS[name], linewidth=0.9)
ax.set_title("Q4: Daily Trading Volume Over Time", color="white")
ax.set_ylabel("Volume (USD)")
ax.legend(facecolor="#160318", labelcolor="white")
plt.tight_layout()
plt.savefig(IMG + "q4_volume_over_time.png", dpi=140)
plt.close()

total_vol = {name: d["Volume"].sum() for name, d in coins.items()}
print("\nQ4 - Total historical volume per coin:", {k: f"{v:,.0f}" for k, v in total_vol.items()})

# ---------------------------------------------------------------------------
# Q5. Which coin grew the most in market cap from listing to 2021 peak?
# ---------------------------------------------------------------------------
print("\nQ5 - Market cap: first recorded vs peak:")
mcap_growth = {}
for name, d in coins.items():
    first, peak = d["Marketcap"].iloc[0], d["Marketcap"].max()
    mult = peak / first if first > 0 else float("nan")
    mcap_growth[name] = mult
    print(f"  {name}: first={first:,.0f}  peak={peak:,.0f}  ({mult:,.0f}x)")

# ---------------------------------------------------------------------------
# Q6. Which coin is the most volatile (daily % return std dev)?
# ---------------------------------------------------------------------------
vol_std = {}
for name, d in coins.items():
    ret = d["Close"].pct_change().dropna()
    vol_std[name] = ret.std() * 100
print("\nQ6 - Daily return volatility (std dev %):", {k: f"{v:.2f}%" for k, v in vol_std.items()})

fig, ax = plt.subplots(figsize=(6, 4))
ax.bar(vol_std.keys(), vol_std.values(), color=[COLORS[n] for n in vol_std])
ax.set_title("Q6: Daily Volatility by Coin (std dev of % change)", color="white")
ax.set_ylabel("Std Dev of Daily Return (%)")
plt.xticks(rotation=15)
plt.tight_layout()
plt.savefig(IMG + "q6_volatility.png", dpi=140)
plt.close()

# ---------------------------------------------------------------------------
# Q7. Do the coins move together? (correlation of daily returns)
# ---------------------------------------------------------------------------
returns = pd.DataFrame({
    name: d.set_index("Date")["Close"].pct_change() for name, d in coins.items()
})
corr = returns.corr()
print("\nQ7 - Correlation of daily returns:\n", corr.round(2))

fig, ax = plt.subplots(figsize=(5.5, 5))
im = ax.imshow(corr, cmap="magma", vmin=0, vmax=1)
ax.set_xticks(range(len(corr)), corr.columns, rotation=30, ha="right")
ax.set_yticks(range(len(corr)), corr.columns)
for i in range(len(corr)):
    for j in range(len(corr)):
        ax.text(j, i, f"{corr.iloc[i, j]:.2f}", ha="center", va="center", color="white")
ax.set_title("Q7: Correlation Between Coins' Daily Returns", color="white")
plt.tight_layout()
plt.savefig(IMG + "q7_correlation.png", dpi=140)
plt.close()

# ---------------------------------------------------------------------------
# Q8. Which year had the most market activity (avg daily volume)?
# ---------------------------------------------------------------------------
all_df["Year"] = all_df["Date"].dt.year
q8 = all_df.groupby("Year")["Volume"].mean()
print("\nQ8 - Avg daily volume (all coins combined) by year:\n", q8)

fig, ax = plt.subplots(figsize=(8, 4))
ax.bar(q8.index.astype(str), q8.values, color=PINK)
ax.set_title("Q8: Average Daily Trading Volume by Year (All Coins)", color="white")
ax.set_ylabel("Avg Volume (USD)")
plt.tight_layout()
plt.savefig(IMG + "q8_volume_by_year.png", dpi=140)
plt.close()

# ---------------------------------------------------------------------------
# Q9. Best single-day gain and worst single-day drop for each coin?
# ---------------------------------------------------------------------------
print("\nQ9 - Best / worst single-day % move:")
for name, d in coins.items():
    ret = d["Close"].pct_change() * 100
    best_i, worst_i = ret.idxmax(), ret.idxmin()
    print(f"  {name}: best +{ret[best_i]:.1f}% on {d['Date'][best_i].date()}  |  "
          f"worst {ret[worst_i]:.1f}% on {d['Date'][worst_i].date()}")

# ---------------------------------------------------------------------------
# Q10. Simple 15-day moving-average trend + forecast cone (mirrors dashboard)
# ---------------------------------------------------------------------------
btc = coins["Bitcoin"].copy()
recent = btc[btc["Date"] >= "2021-04-01"].copy()
recent["MA7"] = recent["High"].rolling(7).mean()

fig, ax = plt.subplots(figsize=(9, 4.5))
ax.plot(recent["Date"], recent["High"], color=PINK, linewidth=1.3, label="Daily High")
ax.plot(recent["Date"], recent["MA7"], color="white", linewidth=1.5, linestyle="--", label="7-day Moving Avg")
ax.set_title("Q10: Bitcoin Daily High, Apr-Jul 2021 (Trend Used for Forecasting)", color="white")
ax.set_ylabel("Price (USD)")
ax.legend(facecolor="#160318", labelcolor="white")
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
plt.tight_layout()
plt.savefig(IMG + "q10_btc_trend_2021.png", dpi=140)
plt.close()

print("\nAll charts saved to analysis/images/")
