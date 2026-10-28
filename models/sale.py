from datetime import datetime
from . import db


class Sale(db.Model):
    """Customer sales transaction with invoice details, discount, and cashier attribution."""

    __tablename__ = "sales"

    id = db.Column(db.Integer, primary_key=True)
    invoice_number = db.Column(db.String(50), unique=True, nullable=False, index=True)
    customer_name = db.Column(db.String(120), nullable=False, default="Walk-in Customer")
    customer_phone = db.Column(db.String(20), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    total_amount = db.Column(db.Float, nullable=False, default=0.0)
    discount_amount = db.Column(db.Float, nullable=False, default=0.0)
    final_amount = db.Column(db.Float, nullable=False, default=0.0)
    payment_mode = db.Column(
        db.String(30), nullable=False, default="Cash"
    )  # 'Cash', 'Card', 'UPI'
    sale_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    items = db.relationship(
        "SaleItem", backref="sale", lazy="dynamic", cascade="all, delete-orphan"
    )

    @property
    def total_items_count(self) -> int:
        return sum(item.quantity for item in self.items)

    def __repr__(self) -> str:
        return f"<Sale {self.invoice_number} (Rs. {self.final_amount:.2f})>"


class SaleItem(db.Model):
    """Individual line item in a sales transaction tied to a specific FEFO batch."""

    __tablename__ = "sale_items"

    id = db.Column(db.Integer, primary_key=True)
    sale_id = db.Column(db.Integer, db.ForeignKey("sales.id"), nullable=False, index=True)
    medicine_id = db.Column(
        db.Integer, db.ForeignKey("medicines.id"), nullable=False, index=True
    )
    batch_id = db.Column(db.Integer, db.ForeignKey("batches.id"), nullable=False, index=True)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)

    def __repr__(self) -> str:
        return f"<SaleItem Med:{self.medicine_id} Batch:{self.batch_id} Qty:{self.quantity}>"
