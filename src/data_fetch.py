"""
data_fetch.py
-------------
Handles all data fetching from Binance via the ccxt library.
- fetch_multiple_cryptos : live snapshot of multiple symbols
- fetch_historical_data  : OHLCV candles for multiple symbols
- save_to_csv            : persist fetched data to data/raw/
"""

import ccxt
import pandas as pd

# Initialize Binance exchange once at module level
binance = ccxt.binance()

# Default symbols used across the project
DEFAULT_SYMBOLS = ["BTC/USDT", "ETH/USDT", "BNB/USDT", "XRP/USDT", "ADA/USDT"]


def fetch_multiple_cryptos(symbols=DEFAULT_SYMBOLS):
    """
    Fetch live ticker data for a list of crypto symbols.

    Parameters
    ----------
    symbols : list of str
        Trading pairs to fetch, e.g. ["BTC/USDT", "ETH/USDT"]

    Returns
    -------
    pd.DataFrame
        Columns: symbol, timestamp, price, volume
    """
    data_list = []
    for symbol in symbols:
        ticker = binance.fetch_ticker(symbol)
        data_list.append({
            "symbol": symbol,
            "timestamp": pd.to_datetime(ticker["timestamp"], unit="ms"),
            "price": ticker["last"],
            "volume": ticker["quoteVolume"],
        })
    return pd.DataFrame(data_list)


def fetch_historical_data(symbols=DEFAULT_SYMBOLS, timeframe="1h", limit=100):
    """
    Fetch historical OHLCV candles for a list of symbols.

    Parameters
    ----------
    symbols   : list of str  – trading pairs
    timeframe : str          – candle size, e.g. "1h", "1d"
    limit     : int          – number of candles to fetch

    Returns
    -------
    dict of {symbol: pd.DataFrame}
        Each DataFrame has columns: timestamp, open, high, low, close, volume
    """
    all_data = {}
    for symbol in symbols:
        ohlcv = binance.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
        df = pd.DataFrame(
            ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"]
        )
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        all_data[symbol] = df
    return all_data


def save_to_csv(historical_data, output_dir="data/raw"):
    """
    Save each symbol's DataFrame to a CSV file.

    Parameters
    ----------
    historical_data : dict of {symbol: pd.DataFrame}
    output_dir      : str – folder to save files into
    """
    import os
    os.makedirs(output_dir, exist_ok=True)
    for symbol, df in historical_data.items():
        filename = f"{symbol.replace('/', '_')}_data.csv"
        filepath = os.path.join(output_dir, filename)
        df.to_csv(filepath, index=False)
        print(f"Saved {symbol} → {filepath}")
