import pytest
from datetime import date, timedelta
from app import create_app
from config import TestingConfig
from models import db, User, Medicine, Batch, Supplier


@pytest.fixture
def app():
    """Create application configured for testing with in-memory database."""
    app = create_app(TestingConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Test HTTP client."""
    return app.test_client()


@pytest.fixture
def test_user(app):
    """Create test pharmacist user."""
    user = User(
        username="testpharm",
        email="pharm@test.com",
        full_name="Test Pharmacist",
        role="Pharmacist",
    )
    user.set_password("pass123")
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture
def sample_inventory(app, test_user):
    """Create supplier, medicine, and batches with varied expiration dates."""
    supplier = Supplier(
        name="Test Distributor",
        lead_time_days=7,
        rating=4.8,
    )
    db.session.add(supplier)
    db.session.commit()

    medicine = Medicine(
        name="Amoxicillin 500mg",
        generic_name="Amoxicillin",
        category="Antibiotic",
        dosage_form="Capsule",
        strength="500mg",
        unit="Strip",
        pack_size=10,
        reorder_level=50,
        supplier_id=supplier.id,
    )
    db.session.add(medicine)
    db.session.commit()

    today = date.today()

    # Batch 1: Expiring soonest (In 15 days) - Should be dispensed first in FEFO!
    b1 = Batch(
        medicine_id=medicine.id,
        batch_number="BATCH-FEFO-01",
        expiry_date=today + timedelta(days=15),
        purchase_price=40.0,
        selling_price=65.0,
        initial_quantity=50,
        current_quantity=30,
        status="Expiring Soon",
    )

    # Batch 2: Expiring later (In 180 days)
    b2 = Batch(
        medicine_id=medicine.id,
        batch_number="BATCH-FEFO-02",
        expiry_date=today + timedelta(days=180),
        purchase_price=40.0,
        selling_price=65.0,
        initial_quantity=100,
        current_quantity=100,
        status="Active",
    )

    # Batch 3: Expired (Expired 10 days ago) - MUST NEVER BE SOLD!
    b3 = Batch(
        medicine_id=medicine.id,
        batch_number="BATCH-EXPIRED",
        expiry_date=today - timedelta(days=10),
        purchase_price=40.0,
        selling_price=65.0,
        initial_quantity=20,
        current_quantity=20,
        status="Expired",
    )

    db.session.add_all([b1, b2, b3])
    db.session.commit()

    return {
        "supplier": supplier,
        "medicine": medicine,
        "batch_first": b1,
        "batch_second": b2,
        "batch_expired": b3,
    }
