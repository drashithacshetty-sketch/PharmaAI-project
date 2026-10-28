import json
from datetime import datetime, date
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models import db, Sale, SaleItem, Medicine, Batch
from services.sales_service import SalesService
from services.inventory_service import InventoryService, InventoryError

sales_bp = Blueprint("sales", __name__)


@sales_bp.route("/")
@login_required
def index():
    """Sales invoices history with invoice search and date filtering."""
    invoice_q = request.args.get("q", "").strip()
    date_filter = request.args.get("date", "").strip()

    query = Sale.query

    if invoice_q:
        query = query.filter(
            (Sale.invoice_number.ilike(f"%{invoice_q}%"))
            | (Sale.customer_name.ilike(f"%{invoice_q}%"))
            | (Sale.customer_phone.ilike(f"%{invoice_q}%"))
        )

    if date_filter:
        try:
            target_dt = datetime.strptime(date_filter, "%Y-%m-%d").date()
            start_dt = datetime.combine(target_dt, datetime.min.time())
            end_dt = datetime.combine(target_dt, datetime.max.time())
            query = query.filter(Sale.sale_date.between(start_dt, end_dt))
        except ValueError:
            pass

    sales = query.order_by(Sale.sale_date.desc()).limit(100).all()

    return render_template(
        "sales/index.html",
        sales=sales,
        invoice_query=invoice_q,
        selected_date=date_filter,
    )


@sales_bp.route("/new", methods=["GET", "POST"])
@login_required
def create():
    """Point of Sale (POS) interface with real-time FEFO allocation preview and checkout."""
    if request.method == "POST":
        customer_name = request.form.get("customer_name", "Walk-in Customer").strip()
        customer_phone = request.form.get("customer_phone", "").strip()
        payment_mode = request.form.get("payment_mode", "Cash").strip()
        discount_amount = float(request.form.get("discount_amount", 0.0) or 0.0)
        items_json = request.form.get("items_json", "[]")

        try:
            items = json.loads(items_json)
        except json.JSONDecodeError:
            flash("Invalid cart data structure.", "danger")
            return redirect(url_for("sales.create"))

        if not items:
            flash("Cannot complete sale: Cart is empty.", "warning")
            return redirect(url_for("sales.create"))

        try:
            sale = SalesService.process_sale(
                customer_name=customer_name,
                customer_phone=customer_phone,
                items=items,
                payment_mode=payment_mode,
                discount_amount=discount_amount,
                user_id=current_user.id,
            )
            flash(f"Invoice {sale.invoice_number} created successfully!", "success")
            return redirect(url_for("sales.receipt", id=sale.id))
        except InventoryError as e:
            flash(f"Checkout Error: {str(e)}", "danger")
            return redirect(url_for("sales.create"))

    # GET: Load medicines with active usable stock for POS autocomplete/selection
    medicines = (
        Medicine.query.filter_by(is_active=True)
        .order_by(Medicine.name.asc())
        .all()
    )
    # Prepare serializable catalogue
    medicines_data = [
        {
            "id": m.id,
            "name": m.name,
            "generic_name": m.generic_name,
            "category": m.category,
            "unit": m.unit,
            "price": m.default_selling_price,
            "usable_stock": m.usable_stock,
        }
        for m in medicines
        if m.usable_stock > 0
    ]

    return render_template(
        "sales/pos.html",
        medicines_json=json.dumps(medicines_data),
        medicines=medicines,
    )


@sales_bp.route("/<int:id>/receipt")
@login_required
def receipt(id: int):
    """View and print pharmacy sales invoice receipt."""
    sale = Sale.query.get_or_404(id)
    return render_template("sales/receipt.html", sale=sale)


@sales_bp.route("/api/fefo-preview/<int:medicine_id>")
@login_required
def fefo_preview(medicine_id: int):
    """API endpoint to preview which batches will be dispensed for a given quantity."""
    quantity = request.args.get("quantity", 1, type=int)
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

    allocations = []
    remaining = quantity
    usable_total = sum(b.current_quantity for b in batches)

    for b in batches:
        if remaining <= 0:
            break
        alloc_qty = min(b.current_quantity, remaining)
        allocations.append(
            {
                "batch_id": b.id,
                "batch_number": b.batch_number,
                "expiry_date": b.expiry_date.strftime("%Y-%m-%d"),
                "days_to_expiry": (b.expiry_date - today).days,
                "allocated_qty": alloc_qty,
                "unit_price": b.selling_price,
            }
        )
        remaining -= alloc_qty

    return jsonify(
        {
            "medicine_id": medicine_id,
            "requested_quantity": quantity,
            "usable_stock": usable_total,
            "is_sufficient": usable_total >= quantity,
            "allocations": allocations,
        }
    )
