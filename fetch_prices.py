"""
scripts/fetch_prices.py
-----------------------
Downloads daily ETF prices via yfinance and saves:
  data/latest_prices.csv        — prices from 2007-01-01 to yesterday
  data/latest_prices_meta.json  — metadata + last_updated timestamp

NOTE: DBO (Invesco DB Oil Fund) data starts January 2007.
      All downloads start from 2007-01-01.

Run manually : python scripts/fetch_prices.py
Run via CI   : triggered hourly by .github/workflows/fetch_prices.yml
"""
import yfinance as yf
import pandas as pd
import json
from datetime import datetime, timezone, timedelta
from pathlib import Path

TICKERS = {"SPY":"Equity","TLT":"Long_Bonds","SHY":"Short_Bonds","GLD":"Gold","DBO":"Oil"}
DATA_START = "2007-01-01"   # DBO hard floor
DATA_END   = datetime.now(timezone.utc).strftime("%Y-%m-%d")  # exclusive — fetches up to yesterday's close

GWP1_SPLITS = {
    "train_start":"2007-01-01","train_end":"2015-12-31",
    "val_start":"2016-01-01","val_end":"2017-12-31",
    "test_start":"2018-01-01",
}

OUTPUT_DIR  = Path(__file__).parent.parent / "data"
PRICES_FILE = OUTPUT_DIR / "latest_prices.csv"
META_FILE   = OUTPUT_DIR / "latest_prices_meta.json"

def fetch():
    print(f"Downloading {list(TICKERS.keys())}  {DATA_START} → {DATA_END} ...")
    data = yf.download(tickers=list(TICKERS.keys()), start=DATA_START, end=DATA_END,
                       auto_adjust=True, progress=False)
    prices = data["Close"].copy()
    if isinstance(prices.columns, pd.MultiIndex):
        prices.columns = prices.columns.get_level_values(0)
    prices = prices.rename(columns=TICKERS)
    prices = prices.dropna(how="all").ffill()
    prices.index.name = "Date"
    prices = prices.reset_index()
    prices["Date"] = prices["Date"].dt.strftime("%Y-%m-%d")
    return prices

def save(prices):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    prices.to_csv(PRICES_FILE, index=False)
    print(f"  Saved {len(prices):,} rows  →  {PRICES_FILE}")

    now_utc   = datetime.now(timezone.utc)
    last_date = prices["Date"].iloc[-1]

    meta = {
        "last_updated":       now_utc.isoformat(),
        "last_updated_human": now_utc.strftime("%b %d %Y, %H:%M UTC"),
        "rows":       len(prices),
        "start_date": prices["Date"].iloc[0],
        "end_date":   last_date,
        "assets":     [c for c in prices.columns if c != "Date"],
        "source":     "yfinance via GitHub Actions",
        "gwp1_splits":{**GWP1_SPLITS, "test_end": last_date},
        "stale_after_hours": 2,
        "data_min_date": DATA_START,
    }
    with open(META_FILE, "w") as f:
        json.dump(meta, f, indent=2)
    print(f"  Saved meta   →  {META_FILE}")
    print(f"  last_updated : {meta['last_updated_human']}")
    print(f"  date range   : {meta['start_date']} → {meta['end_date']}")

if __name__ == "__main__":
    prices = fetch()
    save(prices)
    print("Done.")
