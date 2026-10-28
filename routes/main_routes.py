from datetime import datetime, date, timedelta
from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, login_user, current_user
from sqlalchemy import func
from models import (
    db,
    User,
    Medicine,
    Batch,
    Sale,
    SaleItem,
    DailyMedicineSales,
    PurchaseOrder,
)
from services.inventory_service import InventoryService
from services.reorder_service import ReorderService

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    """Public landing page with interactive FEFO demonstration."""
    return render_template("index.html")


@main_bp.route("/dashboard")
def dashboard():
    """Pharmacy operations and analytics dashboard with automatic guest session bypass."""
    if not current_user.is_authenticated:
        default_user = (
            User.query.filter_by(username="pharmacist").first()
            or User.query.filter_by(username="admin").first()
            or User.query.first()
        )
        if default_user:
            login_user(default_user)
    today = date.today()
    month_start = today.replace(day=1)

    # 1. Total Medicines and Stock Aggregates
    all_medicines = Medicine.query.filter_by(is_active=True).all()
    total_medicines_count = len(all_medicines)
    usable_stock_units = sum(m.usable_stock for m in all_medicines)
    low_stock_medicines = [m for m in all_medicines if m.is_low_stock]
    low_stock_count = len(low_stock_medicines)

    # 2. Expiry Analysis
    expiry_buckets = InventoryService.get_expiry_buckets(critical_days=7, soon_days=30, watch_days=90)
    critical_expiries = expiry_buckets["counts"]["critical"]
    expired_count = expiry_buckets["counts"]["expired"]
    soon_expiries = expiry_buckets["counts"]["soon"]

    # 3. Sales Aggregates
    today_start = datetime.combine(today, datetime.min.time())
    today_sales_val = (
        db.session.query(func.coalesce(func.sum(Sale.final_amount), 0.0))
        .filter(Sale.sale_date >= today_start)
        .scalar()
    )

    month_start_dt = datetime.combine(month_start, datetime.min.time())
    month_sales_val = (
        db.session.query(func.coalesce(func.sum(Sale.final_amount), 0.0))
        .filter(Sale.sale_date >= month_start_dt)
        .scalar()
    )

    # 4. Reorder Alerts
    reorder_recs = ReorderService.get_all_reorder_recommendations(horizon_days=30, only_needed=True)
    urgent_reorders_count = sum(1 for r in reorder_recs if r["urgency"] in ("CRITICAL_STOCKOUT", "HIGH_RISK"))

    # 5. Recent Transactions
    recent_sales = Sale.query.order_by(Sale.sale_date.desc()).limit(6).all()

    # 6. Top 5 Most Sold Medicines (past 30 days)
    thirty_days_ago = today - timedelta(days=30)
    top_sold = (
        db.session.query(
            Medicine.name,
            func.coalesce(func.sum(DailyMedicineSales.total_units_sold), 0).label("units_sold"),
        )
        .join(Medicine, DailyMedicineSales.medicine_id == Medicine.id)
        .filter(DailyMedicineSales.sale_date >= thirty_days_ago)
        .group_by(Medicine.name)
        .order_by(func.sum(DailyMedicineSales.total_units_sold).desc())
        .limit(5)
        .all()
    )

    # 7. Past 7-Day Sales Trend for Chart.js
    trend_labels = []
    trend_values = []
    for i in range(6, -1, -1):
        target_day = today - timedelta(days=i)
        trend_labels.append(target_day.strftime("%a (%d %b)"))
        day_sum = (
            db.session.query(
                func.coalesce(func.sum(DailyMedicineSales.total_units_sold), 0)
            )
            .filter(DailyMedicineSales.sale_date == target_day)
            .scalar()
        )
        trend_values.append(int(day_sum))

    return render_template(
        "dashboard/index.html",
        total_medicines=total_medicines_count,
        usable_stock_units=usable_stock_units,
        low_stock_count=low_stock_count,
        critical_expiries=critical_expiries + expired_count,
        soon_expiries=soon_expiries,
        today_sales=round(float(today_sales_val), 2),
        month_sales=round(float(month_sales_val), 2),
        urgent_reorders_count=urgent_reorders_count,
        reorder_recs=reorder_recs[:5],
        recent_sales=recent_sales,
        top_sold=top_sold,
        trend_labels=trend_labels,
        trend_values=trend_values,
        expiry_chart_data=[
            expired_count,
            critical_expiries,
            soon_expiries,
            expiry_buckets["counts"]["watch"],
            expiry_buckets["counts"]["safe"],
        ],
    )
