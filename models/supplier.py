from datetime import datetime
from . import db


class Supplier(db.Model):
    """Pharmaceutical supplier model for purchase orders and lead time calculations."""

    __tablename__ = "suppliers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False, unique=True, index=True)
    contact_person = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(120), nullable=True)
    phone = db.Column(db.String(30), nullable=True)
    address = db.Column(db.Text, nullable=True)
    lead_time_days = db.Column(
        db.Integer, default=7, nullable=False
    )  # Crucial for reorder point formulas
    rating = db.Column(db.Float, default=4.5)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Relationships
    medicines = db.relationship("Medicine", backref="preferred_supplier", lazy="dynamic")
    purchase_orders = db.relationship("PurchaseOrder", backref="supplier", lazy="dynamic")

    def __repr__(self) -> str:
        return f"<Supplier {self.name} (LeadTime: {self.lead_time_days}d)>"
