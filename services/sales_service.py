from datetime import datetime, date
import uuid
from typing import List, Dict, Any
from models import (
    db,
    Medicine,
    Batch,
    Sale,
    SaleItem,
    DailyMedicineSales,
)
from .inventory_service import InventoryService, InventoryError


class SalesService:
    """Handles sales transactions, FEFO stock reduction, and sales analytics sync."""

    @staticmethod
    def generate_invoice_number() -> str:
        """Generate human-readable unique invoice number."""
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M")
        short_id = uuid.uuid4().hex[:4].upper()
        return f"INV-{timestamp}-{short_id}"

    @staticmethod
    def process_sale(
        customer_name: str,
        customer_phone: str,
        items: List[Dict[str, Any]],
        payment_mode: str = "Cash",
        discount_amount: float = 0.0,
        user_id: int | None = None,
    ) -> Sale:
        """
        Execute an atomic checkout transaction:
        1. Validates all requested medicines and available quantities.
        2. Allocates stock using First Expiry, First Out (FEFO).
        3. Prevents sale of expired batches.
        4. Decrements batch stock and creates line items.
        5. Logs stock movement audit records.
        6. Aggregates daily sales record for AI forecasting.
        """
        if not items:
            raise InventoryError("Cannot process an empty sale. Please add medicines.")

        invoice_number = SalesService.generate_invoice_number()
        total_subtotal = 0.0
        sale_items_to_add: List[SaleItem] = []
        batch_updates: List[tuple[Batch, int]] = []
        movements_data: List[dict] = []
        daily_sales_aggregates: Dict[int, int] = {}  # medicine_id -> total_qty

        # Pre-validate and allocate each item
        for item in items:
            med_id = int(item["medicine_id"])
            qty = int(item["quantity"])

            if qty <= 0:
                raise InventoryError("Item quantity must be at least 1.")

            medicine = Medicine.query.get(med_id)
            if not medicine or not medicine.is_active:
                raise InventoryError(f"Medicine #{med_id} is unavailable or inactive.")

            # FEFO Allocation across non-expired batches
            allocations = InventoryService.allocate_fefo(med_id, qty)

            for batch, alloc_qty in allocations:
                if batch.is_expired:
                    raise InventoryError(
                        f"CRITICAL: Batch {batch.batch_number} for {medicine.name} has expired. "
                        "Expired drugs cannot be dispensed."
                    )

                unit_price = float(batch.selling_price)
                line_subtotal = unit_price * alloc_qty
                total_subtotal += line_subtotal

                sale_item = SaleItem(
                    medicine_id=med_id,
                    batch_id=batch.id,
                    quantity=alloc_qty,
                    unit_price=unit_price,
                    subtotal=line_subtotal,
                )
                sale_items_to_add.append(sale_item)
                batch_updates.append((batch, alloc_qty))

                movements_data.append(
                    {
                        "medicine_id": med_id,
                        "batch_id": batch.id,
                        "alloc_qty": alloc_qty,
                    }
                )

                daily_sales_aggregates[med_id] = (
                    daily_sales_aggregates.get(med_id, 0) + alloc_qty
                )

        # Apply discount safely
        final_amount = max(0.0, total_subtotal - discount_amount)

        try:
            # Create Sale Record
            sale = Sale(
                invoice_number=invoice_number,
                customer_name=customer_name or "Walk-in Customer",
                customer_phone=customer_phone or "",
                user_id=user_id,
                total_amount=round(total_subtotal, 2),
                discount_amount=round(discount_amount, 2),
                final_amount=round(final_amount, 2),
                payment_mode=payment_mode,
                sale_date=datetime.utcnow(),
            )
            db.session.add(sale)
            db.session.flush()  # Populates sale.id

            # Attach sale items and apply batch reductions
            for sale_item in sale_items_to_add:
                sale_item.sale_id = sale.id
                db.session.add(sale_item)

            for batch, deducted_qty in batch_updates:
                batch.current_quantity -= deducted_qty
                batch.refresh_status()

            # Record stock movements
            for mv in movements_data:
                InventoryService.record_stock_movement(
                    medicine_id=mv["medicine_id"],
                    batch_id=mv["batch_id"],
                    movement_type="SALE",
                    quantity_change=-mv["alloc_qty"],
                    reference_type="SALE",
                    reference_id=invoice_number,
                    reason=f"Dispensed in invoice {invoice_number}",
                    user_id=user_id,
                )

            # Update or create DailyMedicineSales for ML and analytics
            today = date.today()
            for med_id, total_units in daily_sales_aggregates.items():
                daily_rec = DailyMedicineSales.query.filter_by(
                    medicine_id=med_id, sale_date=today
                ).first()
                if daily_rec:
                    daily_rec.total_units_sold += total_units
                    daily_rec.num_transactions += 1
                else:
                    daily_rec = DailyMedicineSales(
                        medicine_id=med_id,
                        sale_date=today,
                        total_units_sold=total_units,
                        total_revenue=0.0,
                        num_transactions=1,
                        is_synthetic=False,
                    )
                    db.session.add(daily_rec)

            db.session.commit()
            return sale

        except Exception as e:
            db.session.rollback()
            raise InventoryError(f"Transaction failed: {str(e)}")
