"""
detection.py
------------
Anomaly detection using Isolation Forest.
- train_isolation_forest : fit the model and label anomalies in the DataFrame
- get_anomalies          : return only the anomalous rows
"""

import pandas as pd
from sklearn.ensemble import IsolationForest

FEATURE_COLS = ["price_change", "volume_change", "volatility"]


def train_isolation_forest(df, contamination=0.01, random_state=42):
    """
    Fit an Isolation Forest on the engineered features and annotate the
    DataFrame with an 'anomaly' column.

    Parameters
    ----------
    df            : pd.DataFrame – must contain FEATURE_COLS
    contamination : float        – expected proportion of anomalies (0–0.5)
    random_state  : int          – for reproducibility

    Returns
    -------
    pd.DataFrame – original DataFrame with a new 'anomaly' column
                   where -1 = anomaly, 1 = normal
    """
    missing = [c for c in FEATURE_COLS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing feature columns: {missing}. Run engineer_features() first.")

    df = df.copy()
    X = df[FEATURE_COLS]

    model = IsolationForest(contamination=contamination, random_state=random_state)
    df["anomaly"] = model.fit_predict(X)

    n_anomalies = (df["anomaly"] == -1).sum()
    print(f"Isolation Forest complete — {n_anomalies} anomalies flagged "
          f"out of {len(df)} rows ({contamination*100:.1f}% contamination rate).")

    return df, model


def get_anomalies(df):
    """
    Filter the DataFrame to return only anomalous rows.

    Parameters
    ----------
    df : pd.DataFrame – output of train_isolation_forest()

    Returns
    -------
    pd.DataFrame – rows where anomaly == -1
    """
    if "anomaly" not in df.columns:
        raise ValueError("Run train_isolation_forest() before get_anomalies().")
    return df[df["anomaly"] == -1].copy()
