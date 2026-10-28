from datetime import datetime
from . import db


class DemandPrediction(db.Model):
    """Machine learning forecast predictions with baseline comparison and error bounds."""

    __tablename__ = "demand_predictions"

    id = db.Column(db.Integer, primary_key=True)
    medicine_id = db.Column(
        db.Integer, db.ForeignKey("medicines.id"), nullable=False, index=True
    )
    forecast_date = db.Column(db.Date, nullable=False, index=True)
    horizon_days = db.Column(
        db.Integer, nullable=False, default=7
    )  # Forecast horizon (e.g. 7 or 30 days)
    predicted_units = db.Column(db.Float, nullable=False)
    baseline_units = db.Column(
        db.Float, nullable=False, default=0.0
    )  # Recent average baseline
    model_name = db.Column(db.String(80), nullable=False, default="RandomForestRegressor")
    mae = db.Column(db.Float, nullable=True)  # Mean Absolute Error on test evaluation
    rmse = db.Column(db.Float, nullable=True)  # Root Mean Squared Error
    confidence_lower = db.Column(db.Float, nullable=True)
    confidence_upper = db.Column(db.Float, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self) -> str:
        return f"<DemandPrediction Med:{self.medicine_id} Date:{self.forecast_date} Pred:{self.predicted_units:.1f}>"
