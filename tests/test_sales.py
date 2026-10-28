import pytest
from models import Sale, SaleItem, StockMovement, Batch
from services.sales_service import SalesService
from services.inventory_service import InventoryError


def test_process_sale_success(sample_inventory, test_user):
    """Verify end-to-end checkout transaction, batch stock deduction, and audit movements."""
    med = sample_inventory["medicine"]
    b1 = sample_inventory["batch_first"]
    b2 = sample_inventory["batch_second"]

    initial_b1_qty = b1.current_quantity  # 30

    # Sell 25 units
    items = [{"medicine_id": med.id, "quantity": 25}]
    sale = SalesService.process_sale(
        customer_name="John Doe",
        customer_phone="9988776655",
        items=items,
        payment_mode="UPI",
        discount_amount=25.0,
        user_id=test_user.id,
    )

    assert sale is not None
    assert sale.invoice_number.startswith("INV-")
    assert sale.customer_name == "John Doe"
    # 25 units * 65.0 = 1625.0; - 25.0 discount = 1600.0
    assert sale.total_amount == 1625.0
    assert sale.final_amount == 1600.0

    # Batch 1 quantity must be decremented: 30 - 25 = 5
    b1_refreshed = Batch.query.get(b1.id)
    assert b1_refreshed.current_quantity == 5

    # Stock movement audit record must exist
    movements = StockMovement.query.filter_by(reference_id=sale.invoice_number).all()
    assert len(movements) == 1
    assert movements[0].quantity_change == -25
    assert movements[0].movement_type == "SALE"


def test_process_sale_fails_on_stockout(sample_inventory, test_user):
    """Verify that attempting to sell more units than usable stock fails atomically."""
    med = sample_inventory["medicine"]
    items = [{"medicine_id": med.id, "quantity": 500}]

    with pytest.raises(InventoryError):
        SalesService.process_sale(
            customer_name="Jane Doe",
            customer_phone="",
            items=items,
            user_id=test_user.id,
        )

    # Verify no orphan sale was created
    assert Sale.query.count() == 0
