from datetime import date, timedelta
from models import db, PurchaseOrder, PurchaseOrderItem, DailyMedicineSales
from services.reorder_service import ReorderService


def test_reorder_calculation_and_pack_sizing(sample_inventory):
    """Verify statistical reorder point formulas and supplier pack size rounding."""
    med = sample_inventory["medicine"]
    med.pack_size = 10

    # Seed 30 days of synthetic daily sales (10 units per day)
    today = date.today()
    for i in range(1, 31):
        ds = DailyMedicineSales(
            medicine_id=med.id,
            sale_date=today - timedelta(days=i),
            total_units_sold=10,
            total_revenue=650.0,
            num_transactions=5,
        )
        db.session.add(ds)
    db.session.commit()

    rec = ReorderService.calculate_recommendation(
        medicine=med,
        horizon_days=30,
        service_level_z=1.65,
        lead_time_override=7,
    )

    assert rec["medicine_id"] == med.id
    assert rec["lead_time_days"] == 7
    # μ_d is ~10 units/day
    assert 9.5 <= rec["predicted_daily_demand"] <= 10.5
    # LTD = 10 * 7 = 70 units
    assert 65 <= rec["lead_time_demand"] <= 75
    # Pack size must be respected
    if rec["recommended_units"] > 0:
        assert rec["recommended_units"] % med.pack_size == 0


def test_reorder_accounts_for_incoming_purchase_orders(sample_inventory, test_user):
    """Verify that in-transit purchase orders reduce recommended replenishment quantity."""
    med = sample_inventory["medicine"]
    supplier = sample_inventory["supplier"]

    # Current usable stock: 130 units
    # Add an active Purchase Order for 50 units
    po = PurchaseOrder(
        po_number="PO-TEST-001",
        supplier_id=supplier.id,
        user_id=test_user.id,
        status="Ordered",
        total_amount=2000.0,
    )
    db.session.add(po)
    db.session.flush()

    po_item = PurchaseOrderItem(
        po_id=po.id,
        medicine_id=med.id,
        requested_quantity=50,
        unit_cost=40.0,
        subtotal=2000.0,
        received_quantity=0,
    )
    db.session.add(po_item)
    db.session.commit()

    rec = ReorderService.calculate_recommendation(medicine=med, horizon_days=30)
    assert rec["incoming_stock"] == 50
    assert rec["net_inventory_position"] == rec["usable_stock"] + 50
