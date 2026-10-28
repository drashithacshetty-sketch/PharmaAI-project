from datetime import datetime
from . import db


class StockMovement(db.Model):
    """Immutable audit log for all inventory additions, deductions, sales, and discards."""

    __tablename__ = "stock_movements"

    id = db.Column(db.Integer, primary_key=True)
    medicine_id = db.Column(
        db.Integer, db.ForeignKey("medicines.id"), nullable=False, index=True
    )
    batch_id = db.Column(db.Integer, db.ForeignKey("batches.id"), nullable=True, index=True)
    movement_type = db.Column(
        db.String(30), nullable=False, index=True
    )  # 'SALE', 'PURCHASE_RECEIPT', 'EXPIRED_REMOVAL', 'ADJUSTMENT'
    quantity_change = db.Column(
        db.Integer, nullable=False
    )  # Negative for sales/removal, positive for receipts
    previous_stock = db.Column(db.Integer, nullable=False)
    new_stock = db.Column(db.Integer, nullable=False)
    reference_type = db.Column(
        db.String(30), nullable=True
    )  # 'SALE', 'PO', 'MANUAL_DISCARD'
    reference_id = db.Column(db.String(80), nullable=True)  # Invoice number or PO number
    reason = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)

    # Relationships
    author = db.relationship("User", backref="recorded_movements")

    def __repr__(self) -> str:
        return f"<StockMovement Med:{self.medicine_id} {self.movement_type} {self.quantity_change:+d}>"
