import os
from pathlib import Path
from datetime import date, timedelta
from typing import Dict, Any, List, Tuple
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from .feature_engineering import (
    prepare_features,
    split_train_test_chronological,
    FEATURE_COLS,
    TARGET_COL,
)


class DemandForecaster:
    """
    Supervised Demand Forecasting Engine using Scikit-Learn RandomForestRegressor
    benchmarked against empirical baseline moving averages.
    """

    def __init__(self, model_dir: str | Path = "ml/saved_models"):
        self.model_dir = Path(model_dir)
        self.model_dir.mkdir(parents=True, exist_ok=True)
        self.model_path = self.model_dir / "rf_demand_model.joblib"
        self.model: RandomForestRegressor | None = None
        self.evaluation_metrics: Dict[str, Any] = {}

    def train_and_evaluate(
        self, df_raw: pd.DataFrame, test_days: int = 30
    ) -> Dict[str, Any]:
        """
        Train RandomForestRegressor on chronological train split and evaluate
        against test split and recent-average baseline.
        """
        # Feature preparation without future data leakage
        df_feat = prepare_features(df_raw, drop_na=True)

        train_df, test_df = split_train_test_chronological(df_feat, test_days=test_days)

        X_train = train_df[FEATURE_COLS]
        y_train = train_df[TARGET_COL]

        X_test = test_df[FEATURE_COLS]
        y_test = test_df[TARGET_COL]

        # 1. Baseline Benchmark: Recent 7-Day Moving Average
        # Baseline uses the existing rolling_mean_7 feature as prediction
        baseline_preds = test_df["rolling_mean_7"].values
        baseline_mae = float(mean_absolute_error(y_test, baseline_preds))
        baseline_rmse = float(np.sqrt(mean_squared_error(y_test, baseline_preds)))

        # 2. Train Random Forest Regressor
        self.model = RandomForestRegressor(
            n_estimators=100,
            max_depth=12,
            min_samples_split=4,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=1,
        )
        self.model.fit(X_train, y_train)

        # 3. Model Evaluation on Unseen Test Split
        ml_preds = self.model.predict(X_test)
        # Demand units cannot be negative
        ml_preds = np.clip(ml_preds, 0, None)

        ml_mae = float(mean_absolute_error(y_test, ml_preds))
        ml_rmse = float(np.sqrt(mean_squared_error(y_test, ml_preds)))
        ml_r2 = float(r2_score(y_test, ml_preds))

        # Percentage improvement over baseline
        mae_improvement = (
            ((baseline_mae - ml_mae) / baseline_mae) * 100 if baseline_mae > 0 else 0
        )
        rmse_improvement = (
            ((baseline_rmse - ml_rmse) / baseline_rmse) * 100 if baseline_rmse > 0 else 0
        )

        # Feature importances
        importances = dict(
            zip(FEATURE_COLS, [round(float(x), 4) for x in self.model.feature_importances_])
        )
        sorted_importances = dict(
            sorted(importances.items(), key=lambda item: item[1], reverse=True)
        )

        # Save model artifact
        joblib.dump(self.model, self.model_path)

        self.evaluation_metrics = {
            "baseline": {
                "name": "7-Day Moving Average Baseline",
                "mae": round(baseline_mae, 3),
                "rmse": round(baseline_rmse, 3),
            },
            "random_forest": {
                "name": "RandomForestRegressor (120 trees, max_depth 12)",
                "mae": round(ml_mae, 3),
                "rmse": round(ml_rmse, 3),
                "r2_score": round(ml_r2, 4),
            },
            "improvements": {
                "mae_reduction_percent": round(mae_improvement, 2),
                "rmse_reduction_percent": round(rmse_improvement, 2),
            },
            "feature_importances": sorted_importances,
            "train_samples": len(X_train),
            "test_samples": len(X_test),
        }

        return self.evaluation_metrics

    def load_model(self) -> RandomForestRegressor:
        """Load persisted model artifact from disk."""
        if self.model is None:
            if not self.model_path.exists():
                raise FileNotFoundError(
                    f"Saved model artifact not found at {self.model_path}. "
                    "Run training first."
                )
            self.model = joblib.load(self.model_path)
        return self.model

    def forecast_medicine_demand(
        self,
        medicine_id: int,
        history_df: pd.DataFrame,
        horizon_days: int = 7,
    ) -> List[Dict[str, Any]]:
        """
        Generate recursive multi-step forecasts for horizon_days (e.g. 7 or 30 days).

        DOCUMENTED LIMITATIONS OF MULTI-STEP RECURSIVE FORECASTING:
        1. Error Compounding: Predictions from day T+1 are fed as lag inputs for day T+2.
           Any residual error in early steps propagates and accumulates over a 30-day horizon.
        2. Attenuation/Smoothing: Long-range recursive predictions regress toward the mean,
           potentially underestimating high-frequency spikes.
        3. External Shocks: Unforeseen seasonal disease outbreaks or supply shortages
           cannot be anticipated beyond learned historical periodicity.
        """
        model = self.load_model()

        # Filter strictly for the requested medicine
        med_history = (
            history_df[history_df["medicine_id"] == medicine_id]
            .copy()
            .sort_values("sale_date")
            .reset_index(drop=True)
        )

        if len(med_history) < 35:
            raise ValueError(
                f"At least 35 days of history required for medicine {medicine_id} "
                f"to compute 30-day lookback features. Provided: {len(med_history)}."
            )

        # Working series of known sales and dates
        sales_series = list(med_history[TARGET_COL].values)
        last_date = pd.to_datetime(med_history["sale_date"].iloc[-1]).date()

        forecasts = []
        # Empirical residual std dev for confidence interval estimation
        recent_std = float(np.std(sales_series[-14:])) or 2.0

        for step in range(1, horizon_days + 1):
            target_date = last_date + timedelta(days=step)
            dow = target_date.weekday()
            is_weekend = 1 if dow in (5, 6) else 0
            month = target_date.month
            dom = target_date.day

            # Lag features from working series (1-indexed from end)
            lag_1 = float(sales_series[-1])
            lag_7 = float(sales_series[-7]) if len(sales_series) >= 7 else lag_1
            lag_14 = float(sales_series[-14]) if len(sales_series) >= 14 else lag_1
            lag_21 = float(sales_series[-21]) if len(sales_series) >= 21 else lag_1
            lag_30 = float(sales_series[-30]) if len(sales_series) >= 30 else lag_1

            # Rolling stats on shifted series
            recent_7 = sales_series[-7:]
            recent_14 = sales_series[-14:]
            recent_30 = sales_series[-30:]

            rolling_mean_7 = float(np.mean(recent_7))
            rolling_std_7 = float(np.std(recent_7))
            rolling_mean_14 = float(np.mean(recent_14))
            rolling_mean_30 = float(np.mean(recent_30))

            feat_row = pd.DataFrame(
                [
                    {
                        "lag_1": lag_1,
                        "lag_7": lag_7,
                        "lag_14": lag_14,
                        "lag_21": lag_21,
                        "lag_30": lag_30,
                        "rolling_mean_7": rolling_mean_7,
                        "rolling_std_7": rolling_std_7,
                        "rolling_mean_14": rolling_mean_14,
                        "rolling_mean_30": rolling_mean_30,
                        "day_of_week": dow,
                        "is_weekend": is_weekend,
                        "month": month,
                        "day_of_month": dom,
                    }
                ]
            )[FEATURE_COLS]

            # Model prediction
            predicted_units = float(model.predict(feat_row)[0])
            predicted_units = max(0.0, predicted_units)

            # Baseline comparison (7-day moving average)
            baseline_units = max(0.0, rolling_mean_7)

            # Confidence interval expands slightly with forecast horizon: sigma * (1 + 0.05 * step)
            horizon_penalty = 1.0 + (0.04 * step)
            margin = 1.96 * recent_std * horizon_penalty
            lower_bound = max(0.0, round(predicted_units - margin, 1))
            upper_bound = round(predicted_units + margin, 1)

            forecasts.append(
                {
                    "step": step,
                    "forecast_date": target_date.strftime("%Y-%m-%d"),
                    "day_name": target_date.strftime("%a"),
                    "predicted_units": round(predicted_units, 1),
                    "baseline_units": round(baseline_units, 1),
                    "confidence_lower": lower_bound,
                    "confidence_upper": upper_bound,
                }
            )

            # Append prediction to working series to enable multi-step recursion
            sales_series.append(predicted_units)

        return forecasts
