from datetime import datetime
from . import db


class DailyMedicineSales(db.Model):
    """Daily aggregated sales per medicine for historical analytics and ML training."""

    __tablename__ = "daily_medicine_sales"

    id = db.Column(db.Integer, primary_key=True)
    medicine_id = db.Column(
        db.Integer, db.ForeignKey("medicines.id"), nullable=False, index=True
    )
    sale_date = db.Column(db.Date, nullable=False, index=True)
    total_units_sold = db.Column(db.Integer, nullable=False, default=0)
    total_revenue = db.Column(db.Float, nullable=False, default=0.0)
    num_transactions = db.Column(db.Integer, nullable=False, default=0)
    is_synthetic = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    __table_args__ = (
        db.UniqueConstraint("medicine_id", "sale_date", name="uq_medicine_sale_date"),
    )

    def __repr__(self) -> str:
        return f"<DailySales Med:{self.medicine_id} Date:{self.sale_date} Units:{self.total_units_sold}>"
