import pytest
from services.inventory_service import (
    InventoryService,
    InsufficientStockError,
    InventoryError,
)


def test_usable_stock_excludes_expired_batches(sample_inventory):
    """Verify that medicine.usable_stock only includes non-expired, positive-stock batches."""
    med = sample_inventory["medicine"]
    # Batch 1 (30 units, valid) + Batch 2 (100 units, valid) = 130 usable units
    # Batch 3 (20 units, expired) must NOT be counted!
    assert med.usable_stock == 130
    assert med.total_stock == 150  # includes expired physically


def test_fefo_allocation_priority(sample_inventory):
    """Verify First Expiry, First Out (FEFO) principle: earliest expiring batch is consumed first."""
    med = sample_inventory["medicine"]
    b1 = sample_inventory["batch_first"]
    b2 = sample_inventory["batch_second"]

    # Request 20 units (available in b1 which has 30 units and expires in 15 days)
    allocations = InventoryService.allocate_fefo(med.id, 20)
    assert len(allocations) == 1
    assert allocations[0][0].id == b1.id
    assert allocations[0][1] == 20

    # Request 45 units (should exhaust b1's 30 units, then take 15 from b2)
    allocations_multi = InventoryService.allocate_fefo(med.id, 45)
    assert len(allocations_multi) == 2
    assert allocations_multi[0][0].id == b1.id
    assert allocations_multi[0][1] == 30  # Entire b1
    assert allocations_multi[1][0].id == b2.id
    assert allocations_multi[1][1] == 15  # Remainder from b2


def test_insufficient_stock_raises_error(sample_inventory):
    """Verify InsufficientStockError when requested quantity exceeds total usable stock."""
    med = sample_inventory["medicine"]
    with pytest.raises(InsufficientStockError) as exc_info:
        InventoryService.allocate_fefo(med.id, 200)  # Only 130 usable
    assert "Insufficient usable stock" in str(exc_info.value)


def test_zero_or_negative_quantity_raises_error(sample_inventory):
    """Verify InventoryError on invalid quantity values."""
    med = sample_inventory["medicine"]
    with pytest.raises(InventoryError):
        InventoryService.allocate_fefo(med.id, 0)
    with pytest.raises(InventoryError):
        InventoryService.allocate_fefo(med.id, -10)
