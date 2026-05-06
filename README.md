# crypto-manipulation-detector

Detects potential cryptocurrency price manipulation (pump-and-dump, spoofing, wash trading) using Isolation Forest anomaly detection on Binance OHLCV data.

## Project Structure

```
crypto-manipulation-detector/
├── data/
│   ├── raw/          # CSVs fetched from Binance (auto-generated, git-ignored)
│   └── processed/    # Cleaned / feature-engineered data
├── notebooks/
│   └── analysis.ipynb  # Main analysis notebook
├── src/
│   ├── __init__.py
│   ├── data_fetch.py   # Fetch live + historical data from Binance
│   ├── features.py     # Feature engineering & pump event detection
│   └── detection.py    # Isolation Forest anomaly detection
├── outputs/
│   └── plots/          # Saved matplotlib figures (git-ignored)
├── .gitignore
├── requirements.txt
└── README.md
```

## Setup

```bash
git clone https://github.com/YOUR_USERNAME/crypto-manipulation-detector.git
cd crypto-manipulation-detector
pip install -r requirements.txt
```

## Usage

Open and run `notebooks/analysis.ipynb` top to bottom. It will:
1. Fetch live + historical data from Binance and save CSVs to `data/raw/`
2. Clean the data and engineer features
3. Detect threshold-based pump events
4. Run Isolation Forest to flag anomalies
5. Save plots to `outputs/plots/`

## Tech Stack

- **ccxt** — Binance API wrapper
- **pandas** — data manipulation
- **scikit-learn** — Isolation Forest
- **matplotlib** — visualisation

## Author

Dharmateja PONNAM — Student ID: 20240386
