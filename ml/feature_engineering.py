import pandas as pd
import numpy as np
from typing import Tuple, List

FEATURE_COLS = [
    "lag_1",
    "lag_7",
    "lag_14",
    "lag_21",
    "lag_30",
    "rolling_mean_7",
    "rolling_std_7",
    "rolling_mean_14",
    "rolling_mean_30",
    "day_of_week",
    "is_weekend",
    "month",
    "day_of_month",
]

TARGET_COL = "total_units_sold"


def prepare_features(
    df: pd.DataFrame, drop_na: bool = True
) -> pd.DataFrame:
    """
    Construct time-series lag and rolling statistics without data leakage.

    CRITICAL DATA LEAKAGE PREVENTION:
    All rolling statistics are computed on shifted series (.shift(1)), ensuring
    that the feature values for day T only contain observations from days <= T-1.
    No information from the current day or future days leaks into the feature matrix.
    """
    df = df.copy()
    df["sale_date"] = pd.to_datetime(df["sale_date"])
    df = df.sort_values(by=["medicine_id", "sale_date"]).reset_index(drop=True)

    # Calendar features
    df["day_of_week"] = df["sale_date"].dt.dayofweek
    df["is_weekend"] = df["day_of_week"].isin([5, 6]).astype(int)
    df["month"] = df["sale_date"].dt.month
    df["day_of_month"] = df["sale_date"].dt.day

    # Medicine-grouped lag and rolling metrics
    grouped = df.groupby("medicine_id")[TARGET_COL]

    # Explicit Lags (Units sold k days ago)
    df["lag_1"] = grouped.shift(1)
    df["lag_7"] = grouped.shift(7)
    df["lag_14"] = grouped.shift(14)
    df["lag_21"] = grouped.shift(21)
    df["lag_30"] = grouped.shift(30)

    # Rolling means and standard deviations shifted by 1 to prevent target leakage
    # E.g. rolling_mean_7 for day T is mean of days [T-7, ..., T-1]
    shifted = grouped.shift(1)
    df["rolling_mean_7"] = shifted.groupby(df["medicine_id"]).transform(
        lambda s: s.rolling(7, min_periods=7).mean()
    )
    df["rolling_std_7"] = shifted.groupby(df["medicine_id"]).transform(
        lambda s: s.rolling(7, min_periods=7).std().fillna(0.0)
    )
    df["rolling_mean_14"] = shifted.groupby(df["medicine_id"]).transform(
        lambda s: s.rolling(14, min_periods=14).mean()
    )
    df["rolling_mean_30"] = shifted.groupby(df["medicine_id"]).transform(
        lambda s: s.rolling(30, min_periods=30).mean()
    )

    if drop_na:
        # Drop warm-up window rows where 30-day lag/rolling metrics are unavailable
        df = df.dropna(subset=FEATURE_COLS + [TARGET_COL]).reset_index(drop=True)

    return df


def split_train_test_chronological(
    df: pd.DataFrame, test_days: int = 30
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Chronological train/test split.
    The last `test_days` of history are reserved for evaluation.
    Random shuffling is strictly avoided to preserve temporal integrity.
    """
    max_date = df["sale_date"].max()
    split_cutoff = max_date - pd.Timedelta(days=test_days)

    train_df = df[df["sale_date"] <= split_cutoff].copy()
    test_df = df[df["sale_date"] > split_cutoff].copy()

    return train_df, test_df
