from flask import Blueprint, render_template, request, current_app
from flask_login import login_required
from services.inventory_service import InventoryService

expiry_bp = Blueprint("expiry", __name__)


@expiry_bp.route("/")
@login_required
def index():
    """
    Expiry alert monitoring system.
    Segments stock by configurable thresholds: Expired, Critical (<=7d), Soon (<=30d), Watchlist (<=90d).
    """
    critical_days = request.args.get(
        "critical_days", current_app.config.get("EXPIRY_CRITICAL_DAYS", 7), type=int
    )
    soon_days = request.args.get(
        "soon_days", current_app.config.get("EXPIRY_SOON_DAYS", 30), type=int
    )
    watch_days = request.args.get(
        "watch_days", current_app.config.get("EXPIRY_WATCH_DAYS", 90), type=int
    )

    buckets = InventoryService.get_expiry_buckets(
        critical_days=critical_days,
        soon_days=soon_days,
        watch_days=watch_days,
    )

    return render_template(
        "expiry/index.html",
        buckets=buckets,
        critical_days=critical_days,
        soon_days=soon_days,
        watch_days=watch_days,
    )
