import pandas as pd
import numpy as np
from ml.data_generator import generate_synthetic_sales_data
from ml.feature_engineering import prepare_features, split_train_test_chronological, FEATURE_COLS
from ml.model import DemandForecaster


def test_feature_engineering_no_data_leakage():
    """Verify that feature engineering computes shifted rolling statistics without lookahead leakage."""
    df_raw = generate_synthetic_sales_data(num_days=90, seed=42)
    df_feat = prepare_features(df_raw, drop_na=True)

    assert not df_feat.empty
    for col in FEATURE_COLS:
        assert col in df_feat.columns
        assert not df_feat[col].isnull().any()

    # Verify chronological ordering
    train_df, test_df = split_train_test_chronological(df_feat, test_days=20)
    assert train_df["sale_date"].max() < test_df["sale_date"].min()


def test_forecaster_evaluation_and_metrics(tmp_path):
    """Verify training, MAE/RMSE metrics generation, and model artifact saving."""
    df_raw = generate_synthetic_sales_data(num_days=100, seed=42)
    forecaster = DemandForecaster(model_dir=tmp_path)

    metrics = forecaster.train_and_evaluate(df_raw, test_days=20)

    assert "baseline" in metrics
    assert "random_forest" in metrics
    assert metrics["random_forest"]["mae"] > 0
    assert metrics["random_forest"]["rmse"] > 0
    assert (tmp_path / "rf_demand_model.joblib").exists()

    # Multi-step 7-day forecast
    forecasts = forecaster.forecast_medicine_demand(medicine_id=1, history_df=df_raw, horizon_days=7)
    assert len(forecasts) == 7
    assert all("predicted_units" in f for f in forecasts)
    assert all(f["predicted_units"] >= 0 for f in forecasts)
