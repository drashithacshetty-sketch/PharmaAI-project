from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Medicine, Batch, Supplier, StockMovement
from services.inventory_service import InventoryService

medicine_bp = Blueprint("medicines", __name__)


@medicine_bp.route("/")
@login_required
def index():
    """Medicine inventory catalog with search, category filtering, and stock status indicators."""
    search_query = request.args.get("q", "").strip()
    category_filter = request.args.get("category", "").strip()
    status_filter = request.args.get("status", "").strip()  # 'low_stock', 'out_of_stock'

    query = Medicine.query.filter_by(is_active=True)

    if search_query:
        query = query.filter(
            (Medicine.name.ilike(f"%{search_query}%"))
            | (Medicine.generic_name.ilike(f"%{search_query}%"))
            | (Medicine.category.ilike(f"%{search_query}%"))
        )

    if category_filter:
        query = query.filter(Medicine.category == category_filter)

    medicines = query.order_by(Medicine.name.asc()).all()

    # In-memory status filtering based on dynamic usable stock property
    if status_filter == "low_stock":
        medicines = [m for m in medicines if m.is_low_stock and m.usable_stock > 0]
    elif status_filter == "out_of_stock":
        medicines = [m for m in medicines if m.usable_stock <= 0]

    # Unique categories for the filter dropdown
    categories = (
        db.session.query(Medicine.category)
        .filter(Medicine.is_active == True)
        .distinct()
        .order_by(Medicine.category.asc())
        .all()
    )
    categories = [c[0] for c in categories]

    return render_template(
        "medicines/index.html",
        medicines=medicines,
        categories=categories,
        search_query=search_query,
        selected_category=category_filter,
        selected_status=status_filter,
    )


@medicine_bp.route("/new", methods=["GET", "POST"])
@login_required
def create():
    """Create a new pharmaceutical item."""
    suppliers = Supplier.query.filter_by(is_active=True).order_by(Supplier.name.asc()).all()

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        generic_name = request.form.get("generic_name", "").strip()
        category = request.form.get("category", "").strip()
        dosage_form = request.form.get("dosage_form", "Tablet").strip()
        strength = request.form.get("strength", "").strip()
        unit = request.form.get("unit", "Strip").strip()
        pack_size = int(request.form.get("pack_size", 10))
        reorder_level = int(request.form.get("reorder_level", 50))
        supplier_id = request.form.get("supplier_id")

        if not name or not generic_name or not category:
            flash("Medicine Name, Generic Name, and Category are required.", "danger")
            return render_template("medicines/form.html", suppliers=suppliers, action="create")

        medicine = Medicine(
            name=name,
            generic_name=generic_name,
            category=category,
            dosage_form=dosage_form,
            strength=strength,
            unit=unit,
            pack_size=max(1, pack_size),
            reorder_level=max(1, reorder_level),
            supplier_id=int(supplier_id) if supplier_id else None,
            is_active=True,
        )
        db.session.add(medicine)
        db.session.commit()

        flash(f"Medicine '{medicine.name}' registered successfully.", "success")
        return redirect(url_for("medicines.view", id=medicine.id))

    return render_template("medicines/form.html", suppliers=suppliers, action="create")


@medicine_bp.route("/<int:id>")
@login_required
def view(id: int):
    """View medicine specifications, associated batches, and stock movements."""
    medicine = Medicine.query.get_or_404(id)
    batches = medicine.batches.order_by(Batch.expiry_date.asc()).all()
    movements = (
        StockMovement.query.filter_by(medicine_id=id)
        .order_by(StockMovement.created_at.desc())
        .limit(20)
        .all()
    )

    return render_template(
        "medicines/view.html",
        medicine=medicine,
        batches=batches,
        movements=movements,
    )


@medicine_bp.route("/<int:id>/edit", methods=["GET", "POST"])
@login_required
def edit(id: int):
    """Edit existing medicine details."""
    medicine = Medicine.query.get_or_404(id)
    suppliers = Supplier.query.filter_by(is_active=True).order_by(Supplier.name.asc()).all()

    if request.method == "POST":
        medicine.name = request.form.get("name", "").strip()
        medicine.generic_name = request.form.get("generic_name", "").strip()
        medicine.category = request.form.get("category", "").strip()
        medicine.dosage_form = request.form.get("dosage_form", "Tablet").strip()
        medicine.strength = request.form.get("strength", "").strip()
        medicine.unit = request.form.get("unit", "Strip").strip()
        medicine.pack_size = max(1, int(request.form.get("pack_size", 10)))
        medicine.reorder_level = max(1, int(request.form.get("reorder_level", 50)))

        supplier_id = request.form.get("supplier_id")
        medicine.supplier_id = int(supplier_id) if supplier_id else None

        db.session.commit()
        flash(f"Medicine '{medicine.name}' updated successfully.", "success")
        return redirect(url_for("medicines.view", id=medicine.id))

    return render_template(
        "medicines/form.html",
        medicine=medicine,
        suppliers=suppliers,
        action="edit",
    )
