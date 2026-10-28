from datetime import datetime, date
from . import db


class PurchaseOrder(db.Model):
    """Purchase Order workflow from AI reorder recommendations to physical stock receipt."""

    __tablename__ = "purchase_orders"

    id = db.Column(db.Integer, primary_key=True)
    po_number = db.Column(db.String(50), unique=True, nullable=False, index=True)
    supplier_id = db.Column(
        db.Integer, db.ForeignKey("suppliers.id"), nullable=False, index=True
    )
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    status = db.Column(
        db.String(30), nullable=False, default="Draft", index=True
    )  # 'Draft', 'Ordered', 'Received', 'Cancelled'
    order_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    expected_delivery_date = db.Column(db.Date, nullable=True)
    received_date = db.Column(db.DateTime, nullable=True)
    total_amount = db.Column(db.Float, nullable=False, default=0.0)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    items = db.relationship(
        "PurchaseOrderItem", backref="purchase_order", lazy="dynamic", cascade="all, delete-orphan"
    )

    @property
    def total_ordered_units(self) -> int:
        return sum(item.requested_quantity for item in self.items)

    def __repr__(self) -> str:
        return f"<PurchaseOrder {self.po_number} ({self.status})>"


class PurchaseOrderItem(db.Model):
    """Line item within a purchase order with target quantity and receipt batch metadata."""

    __tablename__ = "purchase_order_items"

    id = db.Column(db.Integer, primary_key=True)
    po_id = db.Column(
        db.Integer, db.ForeignKey("purchase_orders.id"), nullable=False, index=True
    )
    medicine_id = db.Column(
        db.Integer, db.ForeignKey("medicines.id"), nullable=False, index=True
    )
    requested_quantity = db.Column(db.Integer, nullable=False)
    unit_cost = db.Column(db.Float, nullable=False, default=0.0)
    subtotal = db.Column(db.Float, nullable=False, default=0.0)
    received_quantity = db.Column(db.Integer, nullable=False, default=0)
    batch_number = db.Column(db.String(80), nullable=True)
    expiry_date = db.Column(db.Date, nullable=True)

    def __repr__(self) -> str:
        return f"<POItem PO:{self.po_id} Med:{self.medicine_id} Qty:{self.requested_quantity}>"
