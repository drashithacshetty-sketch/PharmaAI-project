import os
import sys
from pathlib import Path
from datetime import date, datetime, timedelta
import pandas as pd

# Add current directory to path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from app import create_app
from config import Config
from models import (
    db,
    User,
    Supplier,
    Medicine,
    Batch,
    Sale,
    SaleItem,
    StockMovement,
    PurchaseOrder,
    PurchaseOrderItem,
    DailyMedicineSales,
    DemandPrediction,
)
from ml.data_generator import generate_synthetic_sales_data, FICTIONAL_MEDICINES
from ml.model import DemandForecaster


def run_seeder():
    """Seed comprehensive demo database with users, catalog, batches, sales, and ML models."""
    app = create_app()

    with app.app_context():
        print("=" * 70)
        print("🌱 PharmaAI — Initializing Database Schema and Seeding Data")
        print("=" * 70)

        # 1. Create all database tables
        db.create_all()
        print("✅ Database tables created successfully.")

        # Check if users already exist
        if User.query.filter_by(username="admin").first():
            print("⚠️ Admin user already exists. Clearing existing data for clean re-seed...")
            db.drop_all()
            db.create_all()

        # 2. Seed Users
        print("\n[1/6] Seeding User Accounts (Admin, Pharmacist, Staff)...")
        admin = User(
            username="admin",
            email="admin@medismart.ai",
            full_name="Dr. Arvind Rao",
            role="Admin",
            is_active=True,
        )
        admin.set_password("admin123")

        pharmacist = User(
            username="pharmacist",
            email="pharmacist@medismart.ai",
            full_name="Priya Sharma",
            role="Pharmacist",
            is_active=True,
        )
        pharmacist.set_password("pharm123")

        staff = User(
            username="staff",
            email="staff@medismart.ai",
            full_name="Kiran Verma",
            role="Staff",
            is_active=True,
        )
        staff.set_password("staff123")

        db.session.add_all([admin, pharmacist, staff])
        db.session.commit()
        print("   - Created admin (admin/admin123)")
        print("   - Created pharmacist (pharmacist/pharm123)")
        print("   - Created staff (staff/staff123)")

        # 3. Seed Suppliers
        print("\n[2/6] Seeding Pharmaceutical Suppliers & Distributors...")
        suppliers_data = [
            {
                "name": "MedVantage Healthcare Logistics",
                "contact_person": "Rajesh Sharma",
                "email": "orders@medvantage.in",
                "phone": "+91 98450 11223",
                "address": "Plot 45, Peenya Industrial Area, Bengaluru, Karnataka 560058",
                "lead_time_days": 5,
                "rating": 4.9,
            },
            {
                "name": "Apex Pharma Distributors",
                "contact_person": "Sunil Mehta",
                "email": "supply@apexpharma.com",
                "phone": "+91 97110 33445",
                "address": "Warehouse 12, MIDC, Andheri East, Mumbai, Maharashtra 400093",
                "lead_time_days": 7,
                "rating": 4.7,
            },
            {
                "name": "Bharat Bio-Logistics Ltd.",
                "contact_person": "Deepak Reddy",
                "email": "info@bharatbiolog.in",
                "phone": "+91 99880 55667",
                "address": "Genome Valley, Shamirpet, Hyderabad, Telangana 500078",
                "lead_time_days": 10,
                "rating": 4.5,
            },
            {
                "name": "CarePoint Generic Supplies",
                "contact_person": "Anita Joseph",
                "email": "dispatch@carepointsupplies.com",
                "phone": "+91 94470 77889",
                "address": "Kinfra Hi-Tech Park, Kalamassery, Kochi, Kerala 683503",
                "lead_time_days": 4,
                "rating": 4.8,
            },
        ]

        created_suppliers = []
        for s_data in suppliers_data:
            s = Supplier(**s_data, is_active=True)
            db.session.add(s)
            created_suppliers.append(s)
        db.session.commit()
        print(f"   - Registered {len(created_suppliers)} supplier vendors.")

        # 4. Seed Medicines
        print("\n[3/6] Seeding Fictional Pharmaceutical Catalog...")
        created_meds = []
        for idx, med_meta in enumerate(FICTIONAL_MEDICINES):
            assigned_supplier = created_suppliers[idx % len(created_suppliers)]
            med = Medicine(
                id=med_meta["id"],
                name=med_meta["name"],
                generic_name=med_meta["generic_name"],
                category=med_meta["category"],
                dosage_form=med_meta["dosage_form"],
                strength=med_meta["strength"],
                unit=med_meta["unit"],
                pack_size=med_meta["pack_size"],
                reorder_level=med_meta["reorder_level"],
                supplier_id=assigned_supplier.id,
                is_active=True,
            )
            db.session.add(med)
            created_meds.append(med)
        db.session.commit()
        print(f"   - Registered {len(created_meds)} pharmaceutical products.")

        # 5. Seed Batches (Varied Expiry Dates to test FEFO, Critical, Soon, Expired, and Depleted)
        print("\n[4/6] Seeding Inventory Batches across Expiry Risk Tiers...")
        today = date.today()
        batch_counter = 1

        for med in created_meds:
            meta = next(m for m in FICTIONAL_MEDICINES if m["id"] == med.id)
            p_price = meta["purchase_price"]
            s_price = meta["selling_price"]

            # Batch 1: Safe Healthy Stock (Expires in 365 days)
            b1 = Batch(
                medicine_id=med.id,
                batch_number=f"BAT-{today.year}-H{batch_counter:02d}",
                expiry_date=today + timedelta(days=365),
                purchase_date=today - timedelta(days=30),
                purchase_price=p_price,
                selling_price=s_price,
                initial_quantity=150,
                current_quantity=120,
                status="Active",
            )
            b1.refresh_status()
            db.session.add(b1)
            db.session.flush()

            StockMovement(
                medicine_id=med.id,
                batch_id=b1.id,
                movement_type="PURCHASE_RECEIPT",
                quantity_change=150,
                previous_stock=0,
                new_stock=150,
                reference_type="PO",
                reference_id="PO-INIT-001",
                reason="Initial inventory receipt",
                user_id=admin.id,
                created_at=datetime.utcnow() - timedelta(days=30),
            )

            # Batch 2: Watchlist Stock (Expires in 75 days)
            b2 = Batch(
                medicine_id=med.id,
                batch_number=f"BAT-{today.year}-W{batch_counter:02d}",
                expiry_date=today + timedelta(days=75),
                purchase_date=today - timedelta(days=60),
                purchase_price=p_price,
                selling_price=s_price,
                initial_quantity=80,
                current_quantity=45,
                status="Active",
            )
            b2.refresh_status()
            db.session.add(b2)
            db.session.flush()

            # Batch 3: Expiring Soon (Expires in 22 days)
            b3 = Batch(
                medicine_id=med.id,
                batch_number=f"BAT-{today.year}-S{batch_counter:02d}",
                expiry_date=today + timedelta(days=22),
                purchase_date=today - timedelta(days=120),
                purchase_price=p_price,
                selling_price=s_price,
                initial_quantity=60,
                current_quantity=20,
                status="Expiring Soon",
            )
            b3.refresh_status()
            db.session.add(b3)

            # For specific medicines, create Critical (<= 7 days) and Expired batches
            if med.id in (1, 3, 6):
                # Critical: Expiring in 4 days
                b_crit = Batch(
                    medicine_id=med.id,
                    batch_number=f"BAT-{today.year}-C{batch_counter:02d}",
                    expiry_date=today + timedelta(days=4),
                    purchase_date=today - timedelta(days=180),
                    purchase_price=p_price,
                    selling_price=s_price,
                    initial_quantity=50,
                    current_quantity=15,
                    status="Expiring Soon",
                )
                b_crit.refresh_status()
                db.session.add(b_crit)

            if med.id in (2, 7):
                # Expired: Expired 12 days ago with non-zero stock to demonstrate safety check
                b_exp = Batch(
                    medicine_id=med.id,
                    batch_number=f"BAT-{today.year-1}-EXP{batch_counter:02d}",
                    expiry_date=today - timedelta(days=12),
                    purchase_date=today - timedelta(days=380),
                    purchase_price=p_price,
                    selling_price=s_price,
                    initial_quantity=40,
                    current_quantity=10,
                    status="Expired",
                )
                b_exp.refresh_status()
                db.session.add(b_exp)

            batch_counter += 1

        db.session.commit()
        print("   - Seeded batches with healthy, watchlist, soon, critical, and expired tiers.")

        # 6. Generate 400 Days of Daily Sales Data & Train ML Model
        print("\n[5/6] Generating 400 Days of Synthetic Sales History & Training ML Model...")
        csv_path = Path(app.config["DATA_PATH"])
        sales_df = generate_synthetic_sales_data(
            num_days=400, output_path=csv_path, seed=42
        )
        print(f"   - Saved {len(sales_df)} daily records to {csv_path}")

        # Bulk insert daily sales records into database
        daily_records = []
        for _, row in sales_df.iterrows():
            rec = DailyMedicineSales(
                medicine_id=int(row["medicine_id"]),
                sale_date=datetime.strptime(row["sale_date"], "%Y-%m-%d").date(),
                total_units_sold=int(row["total_units_sold"]),
                total_revenue=float(row["total_revenue"]),
                num_transactions=int(row["num_transactions"]),
                is_synthetic=True,
            )
            daily_records.append(rec)

        db.session.bulk_save_objects(daily_records)
        db.session.commit()
        print("   - Populated daily_medicine_sales database table.")

        # Train Random Forest Regressor & evaluate against baseline
        print("   - Training RandomForestRegressor with lag features (no data leakage)...")
        forecaster = DemandForecaster(model_dir=app.config["MODEL_DIR"])
        metrics = forecaster.train_and_evaluate(sales_df, test_days=30)
        print(
            f"   - ML Model Trained: Random Forest MAE: {metrics['random_forest']['mae']} "
            f"(vs Baseline MAE: {metrics['baseline']['mae']}, Improvement: {metrics['improvements']['mae_reduction_percent']}%)"
        )

        # Generate and persist 7-day and 30-day forecast predictions
        predictions_to_save = []
        for med in created_meds:
            try:
                preds = forecaster.forecast_medicine_demand(
                    med.id, sales_df, horizon_days=7
                )
                for p in preds:
                    dp = DemandPrediction(
                        medicine_id=med.id,
                        forecast_date=datetime.strptime(p["forecast_date"], "%Y-%m-%d").date(),
                        horizon_days=7,
                        predicted_units=p["predicted_units"],
                        baseline_units=p["baseline_units"],
                        model_name="RandomForestRegressor",
                        mae=metrics["random_forest"]["mae"],
                        rmse=metrics["random_forest"]["rmse"],
                        confidence_lower=p["confidence_lower"],
                        confidence_upper=p["confidence_upper"],
                    )
                    predictions_to_save.append(dp)
            except Exception as e:
                print(f"Warning forecasting for med {med.id}: {e}")

        db.session.bulk_save_objects(predictions_to_save)
        db.session.commit()
        print(f"   - Saved {len(predictions_to_save)} AI forecast predictions to database.")

        # 7. Seed Sample Recent Customer Sales & Purchase Orders
        print("\n[6/6] Seeding Recent Sales Invoices & Procurement Purchase Orders...")
        # Recent Sale 1
        s1 = Sale(
            invoice_number="INV-20261023-A01",
            customer_name="Ramesh Gupta",
            customer_phone="9876543210",
            user_id=pharmacist.id,
            total_amount=250.00,
            discount_amount=10.00,
            final_amount=240.00,
            payment_mode="UPI",
            sale_date=datetime.utcnow() - timedelta(hours=2),
        )
        db.session.add(s1)
        db.session.flush()

        item1 = SaleItem(
            sale_id=s1.id,
            medicine_id=1,
            batch_id=1,
            quantity=10,
            unit_price=25.00,
            subtotal=250.00,
        )
        db.session.add(item1)

        # Recent Sale 2
        s2 = Sale(
            invoice_number="INV-20261023-A02",
            customer_name="Sangeeta Nair",
            customer_phone="9123456780",
            user_id=staff.id,
            total_amount=150.00,
            discount_amount=0.00,
            final_amount=150.00,
            payment_mode="Cash",
            sale_date=datetime.utcnow() - timedelta(hours=5),
        )
        db.session.add(s2)
        db.session.flush()

        item2 = SaleItem(
            sale_id=s2.id,
            medicine_id=2,
            batch_id=4,
            quantity=2,
            unit_price=75.00,
            subtotal=150.00,
        )
        db.session.add(item2)

        # Sample Purchase Order
        po1 = PurchaseOrder(
            po_number="PO-20261020-001",
            supplier_id=created_suppliers[0].id,
            user_id=admin.id,
            status="Ordered",
            order_date=datetime.utcnow() - timedelta(days=2),
            expected_delivery_date=date.today() + timedelta(days=3),
            total_amount=1250.00,
            notes="Replenishment for Paracetamol and Amoxicillin based on 30-day forecast",
        )
        db.session.add(po1)
        db.session.flush()

        po_item1 = PurchaseOrderItem(
            po_id=po1.id,
            medicine_id=1,
            requested_quantity=100,
            unit_cost=12.50,
            subtotal=1250.00,
        )
        db.session.add(po_item1)

        db.session.commit()
        print("   - Seeded recent sales invoices and active purchase orders.")

        print("\n" + "=" * 70)
        print("🎉 PharmaAI Seeding Completed Successfully!")
        print("   Admin Login:      admin / admin123")
        print("   Pharmacist Login: pharmacist / pharm123")
        print("   Staff Login:      staff / staff123")
        print("=" * 70)


if __name__ == "__main__":
    run_seeder()
