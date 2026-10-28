import uuid
from datetime import datetime, date, timedelta
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import (
    db,
    PurchaseOrder,
    PurchaseOrderItem,
    Supplier,
    Medicine,
    Batch,
)
from services.inventory_service import InventoryService

po_bp = Blueprint("purchase_orders", __name__)


@po_bp.route("/")
@login_required
def index():
    """List all purchase orders with procurement status."""
    status_filter = request.args.get("status", "").strip()
    query = PurchaseOrder.query

    if status_filter:
        query = query.filter(PurchaseOrder.status == status_filter)

    orders = query.order_by(PurchaseOrder.created_at.desc()).all()
    return render_template(
        "purchase_orders/index.html",
        orders=orders,
        selected_status=status_filter,
    )


@po_bp.route("/new", methods=["GET", "POST"])
@login_required
def create():
    """Create a new purchase order, optionally pre-filled from smart reorder recommendation."""
    suppliers = Supplier.query.filter_by(is_active=True).order_by(Supplier.name.asc()).all()
    medicines = Medicine.query.filter_by(is_active=True).order_by(Medicine.name.asc()).all()

    prefill_med_id = request.args.get("medicine_id", type=int)
    prefill_qty = request.args.get("quantity", type=int, default=50)

    if request.method == "POST":
        supplier_id = int(request.form.get("supplier_id"))
        expected_days = int(request.form.get("expected_days", 7))
        notes = request.form.get("notes", "").strip()

        # Parse medicine item list from form arrays
        med_ids = request.form.getlist("medicine_id[]")
        quantities = request.form.getlist("quantity[]")
        unit_costs = request.form.getlist("unit_cost[]")

        if not med_ids:
            flash("Please add at least one medicine to the purchase order.", "danger")
            return redirect(url_for("purchase_orders.create"))

        po_number = f"PO-{datetime.utcnow().strftime('%Y%m%d')}-{uuid.uuid4().hex[:4].upper()}"
        expected_delivery = date.today() + timedelta(days=expected_days)

        po = PurchaseOrder(
            po_number=po_number,
            supplier_id=supplier_id,
            user_id=current_user.id,
            status="Ordered",
            order_date=datetime.utcnow(),
            expected_delivery_date=expected_delivery,
            total_amount=0.0,
            notes=notes,
        )
        db.session.add(po)
        db.session.flush()

        total_po_val = 0.0
        for m_id, q_val, c_val in zip(med_ids, quantities, unit_costs):
            qty = int(q_val)
            cost = float(c_val)
            subtotal = qty * cost
            total_po_val += subtotal

            po_item = PurchaseOrderItem(
                po_id=po.id,
                medicine_id=int(m_id),
                requested_quantity=qty,
                unit_cost=cost,
                subtotal=subtotal,
            )
            db.session.add(po_item)

        po.total_amount = round(total_po_val, 2)
        db.session.commit()

        flash(f"Purchase Order {po.po_number} placed successfully!", "success")
        return redirect(url_for("purchase_orders.view", id=po.id))

    return render_template(
        "purchase_orders/form.html",
        suppliers=suppliers,
        medicines=medicines,
        prefill_med_id=prefill_med_id,
        prefill_qty=prefill_qty,
    )


@po_bp.route("/<int:id>")
@login_required
def view(id: int):
    """View purchase order specifications and delivery receipt options."""
    po = PurchaseOrder.query.get_or_404(id)
    return render_template("purchase_orders/view.html", po=po)


@po_bp.route("/<int:id>/receive", methods=["POST"])
@login_required
def receive(id: int):
    """
    Mark purchase order delivery as received:
    Creates physical batches, increments inventory, and logs stock movements.
    """
    po = PurchaseOrder.query.get_or_404(id)

    if po.status == "Received":
        flash("This order has already been received.", "warning")
        return redirect(url_for("purchase_orders.view", id=po.id))

    # For each PO item, read submitted batch number and expiry date
    for item in po.items:
        batch_no = request.form.get(f"batch_number_{item.id}", "").strip().upper()
        exp_date_str = request.form.get(f"expiry_date_{item.id}", "").strip()
        received_qty = int(
            request.form.get(f"received_qty_{item.id}", item.requested_quantity)
        )

        if not batch_no:
            batch_no = f"BATCH-{date.today().strftime('%Y%m')}-{uuid.uuid4().hex[:4].upper()}"

        if exp_date_str:
            try:
                exp_date = datetime.strptime(exp_date_str, "%Y-%m-%d").date()
            except ValueError:
                exp_date = date.today() + timedelta(days=365)
        else:
            exp_date = date.today() + timedelta(days=365)  # 1 year default

        item.received_quantity = received_qty
        item.batch_number = batch_no
        item.expiry_date = exp_date

        # Auto-create new batch for the medicine
        # Selling price set to ~1.4x purchase price if unknown
        selling_price = round(item.unit_cost * 1.45, 2) if item.unit_cost > 0 else 30.0

        batch = Batch(
            medicine_id=item.medicine_id,
            batch_number=batch_no,
            expiry_date=exp_date,
            purchase_date=date.today(),
            purchase_price=item.unit_cost,
            selling_price=selling_price,
            initial_quantity=received_qty,
            current_quantity=received_qty,
            status="Active",
        )
        batch.refresh_status()
        db.session.add(batch)
        db.session.flush()

        # Record stock movement audit log
        InventoryService.record_stock_movement(
            medicine_id=item.medicine_id,
            batch_id=batch.id,
            movement_type="PURCHASE_RECEIPT",
            quantity_change=received_qty,
            reference_type="PO",
            reference_id=po.po_number,
            reason=f"Received via Purchase Order {po.po_number}",
            user_id=current_user.id,
        )

    po.status = "Received"
    po.received_date = datetime.utcnow()
    db.session.commit()

    flash(f"Purchase Order {po.po_number} received! Batches created and inventory updated.", "success")
    return redirect(url_for("purchase_orders.view", id=po.id))


@po_bp.route("/<int:id>/cancel", methods=["POST"])
@login_required
def cancel(id: int):
    """Cancel a pending purchase order."""
    po = PurchaseOrder.query.get_or_404(id)
    if po.status == "Received":
        flash("Cannot cancel a completed/received order.", "danger")
    else:
        po.status = "Cancelled"
        db.session.commit()
        flash(f"Purchase Order {po.po_number} marked as cancelled.", "info")
    return redirect(url_for("purchase_orders.view", id=po.id))
