"""
features.py
-----------
Feature engineering for cryptocurrency manipulation detection.
- load_and_clean  : load a CSV, parse timestamps, drop duplicates/NaNs
- engineer_features : add price_change, volume_change, volatility columns
- detect_pump_events : flag rows where price jumped above a threshold
"""

import pandas as pd


def load_and_clean(filepath):
    """
    Load a raw OHLCV CSV and perform basic cleaning.

    Parameters
    ----------
    filepath : str – path to CSV file, e.g. "data/raw/BTC_USDT_data.csv"

    Returns
    -------
    pd.DataFrame – cleaned DataFrame with parsed timestamps
    """
    df = pd.read_csv(filepath)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.drop_duplicates()
    df = df.reset_index(drop=True)
    print(f"Loaded {len(df)} rows from {filepath}")
    print(f"Missing values:\n{df.isnull().sum()}\n")
    return df


def engineer_features(df):
    """
    Add derived features used by the anomaly detection model.

    Features added
    --------------
    price_change  : % change in closing price vs previous candle
    volume_change : % change in volume vs previous candle
    volatility    : high - low (price range within the candle)

    Parameters
    ----------
    df : pd.DataFrame – cleaned OHLCV DataFrame

    Returns
    -------
    pd.DataFrame – DataFrame with new feature columns, NaNs dropped
    """
    df = df.copy()
    df["price_change"] = df["close"].pct_change() * 100
    df["volume_change"] = df["volume"].pct_change() * 100
    df["volatility"] = df["high"] - df["low"]
    df.dropna(inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df


def detect_pump_events(df, threshold=5.0):
    """
    Simple threshold-based pump detector.
    Flags candles where price rose more than `threshold` % in one period.

    Parameters
    ----------
    df        : pd.DataFrame – must contain a 'price_change' column
    threshold : float        – minimum % rise to count as a pump event

    Returns
    -------
    pd.DataFrame – subset of rows classified as pump events
    """
    if "price_change" not in df.columns:
        raise ValueError("Run engineer_features() before detect_pump_events().")
    pumps = df[df["price_change"] > threshold].copy()
    print(f"Detected {len(pumps)} pump event(s) above {threshold}% threshold.")
    return pumps
