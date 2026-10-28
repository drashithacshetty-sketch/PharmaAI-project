from datetime import datetime, date
from flask import Blueprint, render_template, request, Response
from flask_login import login_required
from services.report_service import ReportService
from models import Medicine, Batch, Sale, DemandPrediction

report_bp = Blueprint("reports", __name__)


@report_bp.route("/")
@login_required
def index():
    """Reports generation and export portal."""
    today = date.today()
    total_medicines = Medicine.query.filter_by(is_active=True).count()
    total_batches = Batch.query.count()
    total_sales_count = Sale.query.count()
    total_forecasts_count = DemandPrediction.query.count()

    return render_template(
        "reports/index.html",
        total_medicines=total_medicines,
        total_batches=total_batches,
        total_sales_count=total_sales_count,
        total_forecasts_count=total_forecasts_count,
        today_date=today.strftime("%Y-%m-%d"),
    )


@report_bp.route("/inventory/csv")
@login_required
def export_inventory_csv():
    """Download full inventory valuation and batch breakdown CSV."""
    csv_data = ReportService.generate_inventory_csv()
    filename = f"medismart_inventory_{date.today().strftime('%Y%m%d')}.csv"
    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )


@report_bp.route("/sales/csv")
@login_required
def export_sales_csv():
    """Download filtered sales transactions CSV."""
    start_str = request.args.get("start_date")
    end_str = request.args.get("end_date")

    start_d = datetime.strptime(start_str, "%Y-%m-%d").date() if start_str else None
    end_d = datetime.strptime(end_str, "%Y-%m-%d").date() if end_str else None

    csv_data = ReportService.generate_sales_csv(start_date=start_d, end_date=end_d)
    filename = f"medismart_sales_{date.today().strftime('%Y%m%d')}.csv"
    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )


@report_bp.route("/expiry/csv")
@login_required
def export_expiry_csv():
    """Download expiry risk and financial exposure CSV."""
    csv_data = ReportService.generate_expiry_csv()
    filename = f"medismart_expiry_risk_{date.today().strftime('%Y%m%d')}.csv"
    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )


@report_bp.route("/forecast/csv")
@login_required
def export_forecast_csv():
    """Download AI demand predictions CSV."""
    csv_data = ReportService.generate_forecast_csv()
    filename = f"medismart_demand_forecast_{date.today().strftime('%Y%m%d')}.csv"
    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )
