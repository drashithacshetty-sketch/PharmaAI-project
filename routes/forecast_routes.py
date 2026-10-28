import os
from pathlib import Path
from datetime import date, timedelta
from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for, current_app
from flask_login import login_required
import pandas as pd
from models import db, Medicine, DailyMedicineSales, DemandPrediction
from ml.model import DemandForecaster
from ml.data_generator import generate_synthetic_sales_data

forecast_bp = Blueprint("forecast", __name__)


def get_sales_history_dataframe(min_days: int = 400) -> pd.DataFrame:
    """Load historical sales records from DB or fallback to synthetic dataset."""
    db_records = DailyMedicineSales.query.order_by(DailyMedicineSales.sale_date.asc()).all()

    if len(db_records) >= 100:
        data = [
            {
                "medicine_id": r.medicine_id,
                "medicine_name": r.medicine.name if r.medicine else f"Medicine {r.medicine_id}",
                "sale_date": r.sale_date.strftime("%Y-%m-%d"),
                "total_units_sold": r.total_units_sold,
                "total_revenue": r.total_revenue,
                "num_transactions": r.num_transactions,
            }
            for r in db_records
        ]
        return pd.DataFrame(data)

    # If DB has insufficient history, read/generate synthetic dataset
    csv_path = Path(current_app.config["DATA_PATH"])
    if not csv_path.exists():
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        generate_synthetic_sales_data(num_days=min_days, output_path=csv_path)

    return pd.read_csv(csv_path)


@forecast_bp.route("/")
@login_required
def index():
    """Demand forecasting dashboard with model evaluation and forecast charts."""
    medicines = Medicine.query.filter_by(is_active=True).order_by(Medicine.name.asc()).all()

    if not medicines:
        flash("No active medicines found in inventory.", "warning")
        return render_template("forecast/index.html", medicines=[], selected_med=None)

    selected_med_id = request.args.get("medicine_id", medicines[0].id, type=int)
    horizon_days = request.args.get("horizon", 7, type=int)
    if horizon_days not in (7, 30):
        horizon_days = 7

    selected_med = Medicine.query.get(selected_med_id) or medicines[0]

    # Load data and run forecaster
    history_df = get_sales_history_dataframe()
    forecaster = DemandForecaster(model_dir=current_app.config["MODEL_DIR"])

    # Ensure model is trained
    if not forecaster.model_path.exists():
        forecaster.train_and_evaluate(history_df, test_days=30)

    # Metrics from forecaster
    eval_metrics = forecaster.evaluation_metrics
    if not eval_metrics:
        # Load or compute quick eval
        eval_metrics = forecaster.train_and_evaluate(history_df, test_days=30)

    # Generate forward predictions
    try:
        forecast_points = forecaster.forecast_medicine_demand(
            medicine_id=selected_med.id,
            history_df=history_df,
            horizon_days=horizon_days,
        )
    except Exception as e:
        flash(f"Forecasting calculation note: {str(e)}", "info")
        forecast_points = []

    # Prepare past 30 days of actuals for visual comparison chart
    med_history = (
        history_df[history_df["medicine_id"] == selected_med.id]
        .sort_values("sale_date")
        .tail(30)
    )

    actual_dates = list(med_history["sale_date"].values)
    actual_units = [int(u) for u in med_history["total_units_sold"].values]

    forecast_dates = [p["forecast_date"] for p in forecast_points]
    forecast_values = [p["predicted_units"] for p in forecast_points]
    baseline_values = [p["baseline_units"] for p in forecast_points]
    confidence_lower = [p["confidence_lower"] for p in forecast_points]
    confidence_upper = [p["confidence_upper"] for p in forecast_points]

    # Combined Timeline for Chart.js
    chart_timeline_labels = actual_dates + forecast_dates
    chart_actual_series = actual_units + [None] * len(forecast_dates)
    chart_forecast_series = [None] * len(actual_dates) + forecast_values
    chart_baseline_series = [None] * len(actual_dates) + baseline_values

    # Calculate total predicted demand for planning horizon
    total_predicted_demand = sum(forecast_values)

    return render_template(
        "forecast/index.html",
        medicines=medicines,
        selected_med=selected_med,
        horizon_days=horizon_days,
        eval_metrics=eval_metrics,
        forecast_points=forecast_points,
        total_predicted_demand=round(total_predicted_demand, 1),
        chart_timeline_labels=chart_timeline_labels,
        chart_actual_series=chart_actual_series,
        chart_forecast_series=chart_forecast_series,
        chart_baseline_series=chart_baseline_series,
        confidence_lower=confidence_lower,
        confidence_upper=confidence_upper,
    )


@forecast_bp.route("/retrain", methods=["POST"])
@login_required
def retrain():
    """Trigger manual re-training of the demand forecasting model."""
    history_df = get_sales_history_dataframe()
    forecaster = DemandForecaster(model_dir=current_app.config["MODEL_DIR"])
    metrics = forecaster.train_and_evaluate(history_df, test_days=30)

    # Persist updated forecasts into DemandPrediction database table
    medicines = Medicine.query.filter_by(is_active=True).all()
    DemandPrediction.query.delete()  # Refresh predictions table

    for med in medicines:
        try:
            preds_7 = forecaster.forecast_medicine_demand(med.id, history_df, horizon_days=7)
            for p in preds_7:
                dp = DemandPrediction(
                    medicine_id=med.id,
                    forecast_date=datetime.strptime(p["forecast_date"], "%Y-%m-%d").date(),
                    horizon_days=7,
                    predicted_units=p["predicted_units"],
                    baseline_units=p["baseline_units"],
                    model_name="RandomForestRegressor",
                    mae=metrics["random_forest"]["mae"],
                    rmse=metrics["random_forest"]["rmse"],
                    confidence_lower=p["confidence_lower"],
                    confidence_upper=p["confidence_upper"],
                )
                db.session.add(dp)
        except Exception:
            continue

    db.session.commit()
    flash(
        f"Model Retrained Successfully! "
        f"MAE: {metrics['random_forest']['mae']} (vs Baseline: {metrics['baseline']['mae']}), "
        f"Improvement: {metrics['improvements']['mae_reduction_percent']}%.",
        "success",
    )
    return redirect(url_for("forecast.index"))


@forecast_bp.route("/api/data/<int:medicine_id>")
@login_required
def api_forecast_data(medicine_id: int):
    """JSON endpoint for asynchronous chart updates."""
    horizon_days = request.args.get("horizon", 7, type=int)
    history_df = get_sales_history_dataframe()
    forecaster = DemandForecaster(model_dir=current_app.config["MODEL_DIR"])

    try:
        points = forecaster.forecast_medicine_demand(medicine_id, history_df, horizon_days=horizon_days)
        return jsonify({"status": "success", "horizon": horizon_days, "points": points})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400
