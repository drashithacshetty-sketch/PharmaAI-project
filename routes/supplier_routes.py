from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from models import db, Supplier

supplier_bp = Blueprint("suppliers", __name__)


@supplier_bp.route("/")
@login_required
def index():
    """List pharmaceutical suppliers and distributors."""
    search_q = request.args.get("q", "").strip()
    query = Supplier.query.filter_by(is_active=True)

    if search_q:
        query = query.filter(
            (Supplier.name.ilike(f"%{search_q}%"))
            | (Supplier.contact_person.ilike(f"%{search_q}%"))
            | (Supplier.email.ilike(f"%{search_q}%"))
        )

    suppliers = query.order_by(Supplier.name.asc()).all()
    return render_template("suppliers/index.html", suppliers=suppliers, search_query=search_q)


@supplier_bp.route("/new", methods=["GET", "POST"])
@login_required
def create():
    """Register a new pharmaceutical vendor."""
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        contact_person = request.form.get("contact_person", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()
        address = request.form.get("address", "").strip()
        lead_time_days = int(request.form.get("lead_time_days", 7))
        rating = float(request.form.get("rating", 4.5))

        if not name:
            flash("Supplier Name is required.", "danger")
            return render_template("suppliers/form.html", action="create")

        supplier = Supplier(
            name=name,
            contact_person=contact_person,
            email=email,
            phone=phone,
            address=address,
            lead_time_days=max(1, lead_time_days),
            rating=min(5.0, max(1.0, rating)),
            is_active=True,
        )
        db.session.add(supplier)
        db.session.commit()

        flash(f"Supplier '{supplier.name}' registered successfully.", "success")
        return redirect(url_for("suppliers.index"))

    return render_template("suppliers/form.html", action="create")


@supplier_bp.route("/<int:id>/edit", methods=["GET", "POST"])
@login_required
def edit(id: int):
    """Edit supplier details and lead times."""
    supplier = Supplier.query.get_or_404(id)

    if request.method == "POST":
        supplier.name = request.form.get("name", "").strip()
        supplier.contact_person = request.form.get("contact_person", "").strip()
        supplier.email = request.form.get("email", "").strip()
        supplier.phone = request.form.get("phone", "").strip()
        supplier.address = request.form.get("address", "").strip()
        supplier.lead_time_days = max(1, int(request.form.get("lead_time_days", 7)))
        supplier.rating = min(5.0, max(1.0, float(request.form.get("rating", 4.5))))

        db.session.commit()
        flash(f"Supplier '{supplier.name}' updated successfully.", "success")
        return redirect(url_for("suppliers.index"))

    return render_template("suppliers/form.html", supplier=supplier, action="edit")
