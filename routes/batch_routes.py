from datetime import datetime, date
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Batch, Medicine
from services.inventory_service import InventoryService, InventoryError

batch_bp = Blueprint("batches", __name__)


@batch_bp.route("/")
@login_required
def index():
    """List batches across all medicines with expiry indicators and stock levels."""
    search_q = request.args.get("q", "").strip()
    status_filter = request.args.get("status", "").strip()

    query = Batch.query.join(Medicine)

    if search_q:
        query = query.filter(
            (Batch.batch_number.ilike(f"%{search_q}%"))
            | (Medicine.name.ilike(f"%{search_q}%"))
        )

    if status_filter:
        query = query.filter(Batch.status == status_filter)

    batches = query.order_by(Batch.expiry_date.asc()).all()

    # Refresh statuses on view
    for b in batches:
        b.refresh_status()
    db.session.commit()

    return render_template(
        "batches/index.html",
        batches=batches,
        search_query=search_q,
        selected_status=status_filter,
    )


@batch_bp.route("/new", methods=["GET", "POST"])
@login_required
def create():
    """Manually register a new delivery batch for a medicine."""
    medicines = Medicine.query.filter_by(is_active=True).order_by(Medicine.name.asc()).all()
    preselected_med_id = request.args.get("medicine_id", type=int)

    if request.method == "POST":
        medicine_id = int(request.form.get("medicine_id"))
        batch_number = request.form.get("batch_number", "").strip().upper()
        expiry_date_str = request.form.get("expiry_date", "")
        purchase_date_str = request.form.get("purchase_date", "") or date.today().strftime("%Y-%m-%d")
        purchase_price = float(request.form.get("purchase_price", 0.0))
        selling_price = float(request.form.get("selling_price", 0.0))
        quantity = int(request.form.get("quantity", 0))

        if not batch_number or not expiry_date_str or quantity <= 0:
            flash("Batch number, valid expiry date, and positive quantity are required.", "danger")
            return render_template("batches/form.html", medicines=medicines, preselected_med_id=medicine_id)

        try:
            exp_date = datetime.strptime(expiry_date_str, "%Y-%m-%d").date()
            purch_date = datetime.strptime(purchase_date_str, "%Y-%m-%d").date()
        except ValueError:
            flash("Invalid date format. Please use YYYY-MM-DD.", "danger")
            return render_template("batches/form.html", medicines=medicines, preselected_med_id=medicine_id)

        if exp_date <= date.today():
            flash("Cannot add a batch that is already expired.", "danger")
            return render_template("batches/form.html", medicines=medicines, preselected_med_id=medicine_id)

        # Create batch
        batch = Batch(
            medicine_id=medicine_id,
            batch_number=batch_number,
            expiry_date=exp_date,
            purchase_date=purch_date,
            purchase_price=purchase_price,
            selling_price=selling_price,
            initial_quantity=quantity,
            current_quantity=quantity,
            status="Active",
        )
        batch.refresh_status()
        db.session.add(batch)
        db.session.flush()

        # Log stock movement
        InventoryService.record_stock_movement(
            medicine_id=medicine_id,
            batch_id=batch.id,
            movement_type="PURCHASE_RECEIPT",
            quantity_change=quantity,
            reference_type="MANUAL_RECEIPT",
            reference_id=batch_number,
            reason=f"Manual batch intake: {quantity} units",
            user_id=current_user.id,
        )

        db.session.commit()
        flash(f"Batch '{batch_number}' registered successfully with {quantity} units.", "success")
        return redirect(url_for("batches.index"))

    return render_template("batches/form.html", medicines=medicines, preselected_med_id=preselected_med_id)


@batch_bp.route("/<int:id>/discard", methods=["POST"])
@login_required
def discard(id: int):
    """Safely discard expired batch stock and record audit trail."""
    reason = request.form.get("reason", "Expired stock safe disposal").strip()
    try:
        batch = InventoryService.discard_expired_batch(
            batch_id=id, user_id=current_user.id, reason=reason
        )
        flash(f"Batch {batch.batch_number} discarded safely. Stock set to 0.", "info")
    except InventoryError as e:
        flash(str(e), "danger")

    return redirect(request.referrer or url_for("expiry.index"))
