from flask import Blueprint, render_template, request, current_app
from flask_login import login_required
from services.reorder_service import ReorderService

reorder_bp = Blueprint("reorder", __name__)


@reorder_bp.route("/")
@login_required
def index():
    """
    Smart Inventory Replenishment recommendations engine.
    Calculates ROP, Lead Time Demand, Safety Stock, and pack-size adjusted order suggestions.
    """
    horizon_days = request.args.get(
        "horizon", current_app.config.get("DEFAULT_HORIZON_DAYS", 30), type=int
    )
    only_needed = request.args.get("filter", "all") == "needed"

    recommendations = ReorderService.get_all_reorder_recommendations(
        horizon_days=horizon_days, only_needed=only_needed
    )

    # Compute summary aggregates
    total_recs = len(recommendations)
    needed_count = sum(1 for r in recommendations if r["needs_reorder"])
    critical_count = sum(
        1 for r in recommendations if r["urgency"] in ("CRITICAL_STOCKOUT", "HIGH_RISK")
    )
    total_estimated_spend = sum(
        r["estimated_order_cost"] for r in recommendations if r["needs_reorder"]
    )

    return render_template(
        "reorder/index.html",
        recommendations=recommendations,
        horizon_days=horizon_days,
        only_needed=only_needed,
        total_recs=total_recs,
        needed_count=needed_count,
        critical_count=critical_count,
        total_estimated_spend=round(total_estimated_spend, 2),
    )
