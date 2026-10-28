from datetime import datetime, date
from . import db


class Batch(db.Model):
    """Pharmaceutical batch tracking with expiration date, cost, and FEFO compatibility."""

    __tablename__ = "batches"

    id = db.Column(db.Integer, primary_key=True)
    medicine_id = db.Column(
        db.Integer, db.ForeignKey("medicines.id"), nullable=False, index=True
    )
    batch_number = db.Column(db.String(80), nullable=False, index=True)
    expiry_date = db.Column(db.Date, nullable=False, index=True)
    purchase_date = db.Column(db.Date, default=date.today, nullable=False)
    purchase_price = db.Column(db.Float, nullable=False, default=0.0)
    selling_price = db.Column(db.Float, nullable=False, default=0.0)
    initial_quantity = db.Column(db.Integer, nullable=False)
    current_quantity = db.Column(db.Integer, nullable=False)
    status = db.Column(
        db.String(30), nullable=False, default="Active"
    )  # 'Active', 'Expiring Soon', 'Expired', 'Depleted'
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    stock_movements = db.relationship("StockMovement", backref="batch", lazy="dynamic")
    sale_items = db.relationship("SaleItem", backref="batch", lazy="dynamic")

    @property
    def days_until_expiry(self) -> int:
        """Days remaining until batch expires. Negative if already expired."""
        return (self.expiry_date - date.today()).days

    @property
    def is_expired(self) -> bool:
        """True if the batch is already expired."""
        return self.expiry_date <= date.today()

    @property
    def expiry_urgency(self) -> str:
        """
        Urgency category:
        - 'EXPIRED': <= 0 days
        - 'CRITICAL': <= 7 days
        - 'SOON': <= 30 days
        - 'WATCH': <= 90 days
        - 'NORMAL': > 90 days
        """
        days = self.days_until_expiry
        if days <= 0:
            return "EXPIRED"
        elif days <= 7:
            return "CRITICAL"
        elif days <= 30:
            return "SOON"
        elif days <= 90:
            return "WATCH"
        return "NORMAL"

    def refresh_status(self) -> str:
        """Recalculate batch status based on stock and expiry date."""
        if self.current_quantity <= 0:
            self.status = "Depleted"
        elif self.is_expired:
            self.status = "Expired"
        elif self.days_until_expiry <= 30:
            self.status = "Expiring Soon"
        else:
            self.status = "Active"
        return self.status

    def __repr__(self) -> str:
        return f"<Batch {self.batch_number} (Exp: {self.expiry_date}, Qty: {self.current_quantity})>"
