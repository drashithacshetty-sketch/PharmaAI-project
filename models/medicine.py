from datetime import datetime, date
from . import db


class Medicine(db.Model):
    """Pharmaceutical item with stock aggregations, pack sizing, and reorder levels."""

    __tablename__ = "medicines"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False, index=True)
    generic_name = db.Column(db.String(150), nullable=False, index=True)
    category = db.Column(db.String(80), nullable=False, index=True)
    dosage_form = db.Column(db.String(50), nullable=False)  # Tablet, Capsule, Syrup, etc.
    strength = db.Column(db.String(50), nullable=True)  # e.g., 500mg, 10mg/5ml
    unit = db.Column(db.String(30), nullable=False, default="Strip")  # Strip, Box, Bottle, Vial
    pack_size = db.Column(
        db.Integer, nullable=False, default=10
    )  # Minimum pack bundle for ordering
    reorder_level = db.Column(
        db.Integer, nullable=False, default=50
    )  # Static baseline reorder trigger
    supplier_id = db.Column(db.Integer, db.ForeignKey("suppliers.id"), nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Relationships
    batches = db.relationship(
        "Batch", backref="medicine", lazy="dynamic", cascade="all, delete-orphan"
    )
    daily_sales = db.relationship(
        "DailyMedicineSales", backref="medicine", lazy="dynamic", cascade="all, delete-orphan"
    )
    predictions = db.relationship(
        "DemandPrediction", backref="medicine", lazy="dynamic", cascade="all, delete-orphan"
    )
    stock_movements = db.relationship(
        "StockMovement", backref="medicine", lazy="dynamic", cascade="all, delete-orphan"
    )
    po_items = db.relationship("PurchaseOrderItem", backref="medicine", lazy="dynamic")
    sale_items = db.relationship("SaleItem", backref="medicine", lazy="dynamic")

    @property
    def usable_stock(self) -> int:
        """Total current quantity across all non-expired active batches."""
        today = date.today()
        usable_batches = [
            b for b in self.batches if b.current_quantity > 0 and b.expiry_date > today
        ]
        return sum(b.current_quantity for b in usable_batches)

    @property
    def total_stock(self) -> int:
        """Total quantity across all batches regardless of expiry status."""
        return sum(b.current_quantity for b in self.batches)

    @property
    def is_low_stock(self) -> bool:
        """True if usable stock is at or below the reorder level."""
        return self.usable_stock <= self.reorder_level

    @property
    def default_selling_price(self) -> float:
        """Latest active batch price, or 0.0."""
        latest_batch = (
            self.batches.filter_by(status="Active")
            .order_by(db.desc("created_at"))
            .first()
        )
        return float(latest_batch.selling_price) if latest_batch else 0.0

    def __repr__(self) -> str:
        return f"<Medicine {self.name} ({self.strength}) - Stock: {self.usable_stock}>"
