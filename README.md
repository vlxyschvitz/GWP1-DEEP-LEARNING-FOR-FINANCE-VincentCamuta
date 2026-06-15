# GWP1 · Deep Learning for Finance — Interactive Dashboard
**MScFE 642 · Group Work Project 1**

Interactive multi-asset ETF analysis dashboard using MLP, CNN-GAF, LSTM, and Multi-Output LSTM.
Runs entirely in the browser — no backend server required.
Real price data is fetched automatically via GitHub Actions every hour.

---

## Live Demo
After setup, your dashboard is live at:
```
https://YOUR_USERNAME.github.io/YOUR_REPO_NAME/
```

---

## How It Works

```
GitHub Actions (every hour)
  └─ scripts/fetch_prices.py
        └─ yfinance: downloads SPY TLT SHY GLD DBO from 2007-01-01 → yesterday
        └─ saves  data/latest_prices.csv
        └─ saves  data/latest_prices_meta.json  ← "last_updated" timestamp
              ↓
index.html (browser — no server)
  └─ fetches CSV + meta from raw.githubusercontent.com
  └─ shows  ✅ Last updated: Jun 13 2026, 10:10 UTC · Data delayed ~1 hr
  └─ if fetch fails → bundled fallback demo data (2007–yesterday, simulated)
        └─ shows ⚠️ Using bundled fallback data
```

---

## Setup (5 minutes)

### 1 · Fork or clone this repo
```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO
```

### 2 · Edit index.html — fill in your repo details
Open `index.html`, find these two lines near the top of the `<script>` block:
```js
const GITHUB_USER = 'YOUR_GITHUB_USERNAME';   // ← your GitHub username
const GITHUB_REPO = 'YOUR_REPO_NAME';          // ← your repo name
```

### 3 · Seed real data locally (one-time)
```bash
pip install yfinance pandas
python scripts/fetch_prices.py
git add data/
git commit -m "data: initial ETF prices 2007–present"
git push
```

### 4 · Enable GitHub Pages
Repo → **Settings → Pages → Source: Deploy from branch → main / root → Save**

### 5 · Verify GitHub Actions
Repo → **Actions → Fetch ETF Prices → Run workflow** (first manual trigger)
After success it runs automatically every hour.

---

## Repo Structure

```
your-repo/
├── index.html                         ← Entire dashboard (HTML + CSS + JS)
├── requirements.txt                   ← Python deps for GitHub Actions
├── .gitignore
├── README.md
├── scripts/
│   └── fetch_prices.py               ← Price downloader
├── .github/
│   └── workflows/
│       └── fetch_prices.yml          ← Hourly GitHub Actions schedule
└── data/
    ├── latest_prices.csv             ← Auto-updated hourly
    └── latest_prices_meta.json       ← Timestamp + split defaults + metadata
```

---

## Default Timeline (GWP1 Project)

| Period     | Start       | End         | Notes                            |
|------------|-------------|-------------|----------------------------------|
| Training   | 2007-01-01  | 2015-12-31  | DBO available from Jan 2007      |
| Validation | 2016-01-01  | 2017-12-31  |                                  |
| Test       | 2018-01-01  | 2022-12-30  | GWP1 mandated test period        |

Users can freely change these in the dashboard — all steps re-run with the new periods.

### Timeline rules enforced
- All dates must be **≥ 2007-01-01** — DBO (Oil ETF) data constraint
- Test end cannot exceed **last available data date** (yesterday)
- Periods must be **chronological and non-overlapping**
- Error banner appears immediately if any rule is violated

---

## Data Banner States

| Banner | Meaning |
|--------|---------|
| ✅ Green | Live GitHub data loaded — timestamp shown |
| ⚠️ Amber | GitHub fetch failed — using bundled fallback |
| ❌ Red   | Config error — check GITHUB_USER / GITHUB_REPO |

---

## ETFs Covered

| Symbol | Asset Class  | Notes                         |
|--------|-------------|-------------------------------|
| SPY    | Equity       | SPDR S&P 500 ETF              |
| TLT    | Long Bonds   | iShares 20+ Year Treasury     |
| SHY    | Short Bonds  | iShares 1-3 Year Treasury     |
| GLD    | Gold         | SPDR Gold Shares              |
| DBO    | Oil          | Invesco DB Oil Fund (from 2007)|

---

## Notes
- Data delayed ~1 hour (end-of-day prices, updated every hour)
- Free — no API keys, no backend, no hosting costs
- Dashboard works offline using bundled fallback data if GitHub is unreachable
