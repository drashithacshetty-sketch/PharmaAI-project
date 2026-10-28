from datetime import date, timedelta
from models import db, Batch, StockMovement
from services.inventory_service import InventoryService


def test_expiry_bucket_classification(sample_inventory):
    """Verify that batches are accurately segmented by configurable expiration days."""
    b1 = sample_inventory["batch_first"]   # expires in 15 days -> 'soon' (<=30)
    b2 = sample_inventory["batch_second"]  # expires in 180 days -> 'safe' (>90)
    b3 = sample_inventory["batch_expired"] # expired 10 days ago -> 'expired'

    buckets = InventoryService.get_expiry_buckets(critical_days=7, soon_days=30, watch_days=90)

    assert buckets["counts"]["expired"] >= 1
    assert any(b.id == b3.id for b in buckets["expired"])

    assert buckets["counts"]["soon"] >= 1
    assert any(b.id == b1.id for b in buckets["soon"])

    assert buckets["counts"]["safe"] >= 1
    assert any(b.id == b2.id for b in buckets["safe"])


def test_discard_expired_batch(sample_inventory, test_user):
    """Verify safe removal of expired stock with audit trail logging."""
    b_exp = sample_inventory["batch_expired"]
    initial_qty = b_exp.current_quantity

    discarded = InventoryService.discard_expired_batch(
        batch_id=b_exp.id,
        user_id=test_user.id,
        reason="Routine safety disposal of expired antibiotics",
    )

    assert discarded.current_quantity == 0
    assert discarded.status == "Expired"

    # Audit log check
    movement = StockMovement.query.filter_by(
        batch_id=b_exp.id, movement_type="EXPIRED_REMOVAL"
    ).first()
    assert movement is not None
    assert movement.quantity_change == -initial_qty
