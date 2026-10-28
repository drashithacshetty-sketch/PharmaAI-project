from datetime import date, datetime
from typing import List, Tuple, Dict, Any
from models import db, Medicine, Batch, StockMovement


class InventoryError(Exception):
    """Custom exception for inventory validation and stock constraints."""
    pass


class ExpiredBatchError(InventoryError):
    """Raised when an operation attempts to allocate or sell an expired batch."""
    pass


class InsufficientStockError(InventoryError):
    """Raised when available usable stock is less than the requested quantity."""
    pass


class InventoryService:
    """Core inventory logic implementing FEFO allocation, stock movements, and batch management."""

    @staticmethod
    def get_fefo_batches(medicine_id: int) -> List[Batch]:
        """
        Fetch all eligible, non-expired batches for a medicine sorted by Expiry Date ASC.
        First Expiry, First Out (FEFO) principle ensures oldest valid stock is dispensed first.
        """
        today = date.today()
        batches = (
            Batch.query.filter(
                Batch.medicine_id == medicine_id,
                Batch.current_quantity > 0,
                Batch.expiry_date > today,
            )
            .order_by(Batch.expiry_date.asc())
            .all()
        )
        return batches

    @staticmethod
    def allocate_fefo(medicine_id: int, quantity: int) -> List[Tuple[Batch, int]]:
        """
        Allocate required quantity from batches using FEFO.
        Raises InsufficientStockError if requested quantity exceeds non-expired usable stock.
        Returns list of (batch, allocated_quantity) pairs.
        """
        if quantity <= 0:
            raise InventoryError("Requested quantity must be greater than zero.")

        medicine = Medicine.query.get(medicine_id)
        if not medicine:
            raise InventoryError(f"Medicine with ID {medicine_id} not found.")

        batches = InventoryService.get_fefo_batches(medicine_id)
        usable_stock = sum(b.current_quantity for b in batches)

        if quantity > usable_stock:
            raise InsufficientStockError(
                f"Insufficient usable stock for {medicine.name}. "
                f"Requested: {quantity}, Usable Non-Expired Stock: {usable_stock}."
            )

        allocations: List[Tuple[Batch, int]] = []
        remaining = quantity

        for batch in batches:
            if remaining <= 0:
                break

            alloc_qty = min(batch.current_quantity, remaining)
            allocations.append((batch, alloc_qty))
            remaining -= alloc_qty

        return allocations

    @staticmethod
    def record_stock_movement(
        medicine_id: int,
        batch_id: int | None,
        movement_type: str,
        quantity_change: int,
        reference_type: str,
        reference_id: str,
        reason: str,
        user_id: int | None = None,
    ) -> StockMovement:
        """
        Records an audit log entry in the stock_movements table.
        Captures previous and new stock levels for transparency.
        """
        medicine = Medicine.query.get(medicine_id)
        if not medicine:
            raise InventoryError(f"Medicine with ID {medicine_id} not found.")

        # Compute previous stock before this change
        current_usable = medicine.usable_stock
        new_usable = current_usable + quantity_change

        movement = StockMovement(
            medicine_id=medicine_id,
            batch_id=batch_id,
            movement_type=movement_type,
            quantity_change=quantity_change,
            previous_stock=current_usable,
            new_stock=new_usable,
            reference_type=reference_type,
            reference_id=reference_id,
            reason=reason,
            user_id=user_id,
            created_at=datetime.utcnow(),
        )
        db.session.add(movement)
        return movement

    @staticmethod
    def get_expiry_buckets(
        critical_days: int = 7, soon_days: int = 30, watch_days: int = 90
    ) -> Dict[str, Any]:
        """
        Segment all active inventory batches into configurable expiry risk buckets:
        - Expired (already expired)
        - Critical (expiring in <= critical_days)
        - Soon (expiring in <= soon_days)
        - Watch (expiring in <= watch_days)
        - Safe (> watch_days)
        """
        today = date.today()
        batches = Batch.query.filter(Batch.current_quantity > 0).all()

        expired = []
        critical = []
        soon = []
        watch = []
        safe = []

        for b in batches:
            days = (b.expiry_date - today).days
            if days <= 0:
                expired.append(b)
            elif days <= critical_days:
                critical.append(b)
            elif days <= soon_days:
                soon.append(b)
            elif days <= watch_days:
                watch.append(b)
            else:
                safe.append(b)

        # Sort each bucket by expiry date
        expired.sort(key=lambda x: x.expiry_date)
        critical.sort(key=lambda x: x.expiry_date)
        soon.sort(key=lambda x: x.expiry_date)
        watch.sort(key=lambda x: x.expiry_date)

        return {
            "expired": expired,
            "critical": critical,
            "soon": soon,
            "watch": watch,
            "safe": safe,
            "counts": {
                "expired": len(expired),
                "critical": len(critical),
                "soon": len(soon),
                "watch": len(watch),
                "safe": len(safe),
                "total_monitored": len(batches),
            },
            "financial_risk": {
                "expired_loss": sum(b.current_quantity * b.purchase_price for b in expired),
                "critical_value": sum(b.current_quantity * b.purchase_price for b in critical),
                "soon_value": sum(b.current_quantity * b.purchase_price for b in soon),
            },
        }

    @staticmethod
    def discard_expired_batch(batch_id: int, user_id: int | None, reason: str = "Expired stock discarded") -> Batch:
        """
        Safely remove an expired batch from usable stock and log audit movement.
        """
        batch = Batch.query.get(batch_id)
        if not batch:
            raise InventoryError(f"Batch with ID {batch_id} not found.")

        qty_to_remove = batch.current_quantity
        if qty_to_remove <= 0:
            raise InventoryError("Batch has zero stock; nothing to discard.")

        batch.current_quantity = 0
        batch.status = "Expired"

        InventoryService.record_stock_movement(
            medicine_id=batch.medicine_id,
            batch_id=batch.id,
            movement_type="EXPIRED_REMOVAL",
            quantity_change=-qty_to_remove,
            reference_type="MANUAL_DISCARD",
            reference_id=f"DISCARD-{batch.batch_number}",
            reason=reason,
            user_id=user_id,
        )
        db.session.commit()
        return batch
