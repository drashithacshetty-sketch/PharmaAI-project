import csv
import io
from datetime import datetime, date
from typing import Optional
from models import Medicine, Batch, Sale, SaleItem, DemandPrediction, DailyMedicineSales
from .inventory_service import InventoryService


class ReportService:
    """Generates analytical summaries and CSV data exports for pharmacy reporting."""

    @staticmethod
    def generate_inventory_csv() -> str:
        """Export complete inventory valuation, batch details, and stock statuses to CSV."""
        output = io.StringIO()
        writer = csv.writer(output)

        writer.writerow(
            [
                "Medicine ID",
                "Medicine Name",
                "Generic Name",
                "Category",
                "Dosage Form",
                "Batch Number",
                "Expiry Date",
                "Days to Expiry",
                "Purchase Price (INR)",
                "Selling Price (INR)",
                "Current Qty",
                "Batch Valuation (INR)",
                "Batch Status",
                "Preferred Supplier",
            ]
        )

        batches = (
            Batch.query.join(Medicine)
            .order_by(Medicine.name.asc(), Batch.expiry_date.asc())
            .all()
        )

        today = date.today()
        for b in batches:
            med = b.medicine
            supplier_name = (
                med.preferred_supplier.name if med.preferred_supplier else "N/A"
            )
            valuation = round(b.current_quantity * b.purchase_price, 2)
            days_to_exp = (b.expiry_date - today).days

            writer.writerow(
                [
                    med.id,
                    med.name,
                    med.generic_name,
                    med.category,
                    med.dosage_form,
                    b.batch_number,
                    b.expiry_date.strftime("%Y-%m-%d"),
                    days_to_exp,
                    f"{b.purchase_price:.2f}",
                    f"{b.selling_price:.2f}",
                    b.current_quantity,
                    f"{valuation:.2f}",
                    b.status,
                    supplier_name,
                ]
            )

        return output.getvalue()

    @staticmethod
    def generate_sales_csv(start_date: Optional[date] = None, end_date: Optional[date] = None) -> str:
        """Export sales transactions with invoice numbers, items, amounts, and dates."""
        output = io.StringIO()
        writer = csv.writer(output)

        writer.writerow(
            [
                "Invoice Number",
                "Sale Date",
                "Customer Name",
                "Customer Phone",
                "Medicine Name",
                "Batch Number",
                "Quantity Sold",
                "Unit Price (INR)",
                "Item Subtotal (INR)",
                "Total Invoice Amount (INR)",
                "Discount (INR)",
                "Final Amount (INR)",
                "Payment Mode",
                "Billed By",
            ]
        )

        query = Sale.query
        if start_date:
            query = query.filter(Sale.sale_date >= datetime.combine(start_date, datetime.min.time()))
        if end_date:
            query = query.filter(Sale.sale_date <= datetime.combine(end_date, datetime.max.time()))

        sales = query.order_by(Sale.sale_date.desc()).all()

        for sale in sales:
            cashier_name = sale.cashier.username if sale.cashier else "System"
            for item in sale.items:
                writer.writerow(
                    [
                        sale.invoice_number,
                        sale.sale_date.strftime("%Y-%m-%d %H:%M"),
                        sale.customer_name,
                        sale.customer_phone or "N/A",
                        item.medicine.name if item.medicine else "Unknown",
                        item.batch.batch_number if item.batch else "Unknown",
                        item.quantity,
                        f"{item.unit_price:.2f}",
                        f"{item.subtotal:.2f}",
                        f"{sale.total_amount:.2f}",
                        f"{sale.discount_amount:.2f}",
                        f"{sale.final_amount:.2f}",
                        sale.payment_mode,
                        cashier_name,
                    ]
                )

        return output.getvalue()

    @staticmethod
    def generate_expiry_csv() -> str:
        """Export all expiring and expired batches with financial risk metrics."""
        output = io.StringIO()
        writer = csv.writer(output)

        writer.writerow(
            [
                "Medicine Name",
                "Generic Name",
                "Batch Number",
                "Expiry Date",
                "Days Remaining",
                "Urgency Level",
                "Current Stock Qty",
                "Purchase Price (INR)",
                "At-Risk Valuation (INR)",
                "Supplier",
            ]
        )

        buckets = InventoryService.get_expiry_buckets()
        all_expiring = (
            buckets["expired"] + buckets["critical"] + buckets["soon"] + buckets["watch"]
        )

        today = date.today()
        for b in all_expiring:
            med = b.medicine
            supplier_name = (
                med.preferred_supplier.name if med.preferred_supplier else "N/A"
            )
            days = (b.expiry_date - today).days
            at_risk_val = round(b.current_quantity * b.purchase_price, 2)

            writer.writerow(
                [
                    med.name,
                    med.generic_name,
                    b.batch_number,
                    b.expiry_date.strftime("%Y-%m-%d"),
                    days,
                    b.expiry_urgency,
                    b.current_quantity,
                    f"{b.purchase_price:.2f}",
                    f"{at_risk_val:.2f}",
                    supplier_name,
                ]
            )

        return output.getvalue()

    @staticmethod
    def generate_forecast_csv() -> str:
        """Export machine learning demand forecast projections and actual benchmarks."""
        output = io.StringIO()
        writer = csv.writer(output)

        writer.writerow(
            [
                "Medicine ID",
                "Medicine Name",
                "Forecast Date",
                "Horizon (Days)",
                "Predicted Units",
                "Baseline Units",
                "Model",
                "MAE",
                "RMSE",
                "Lower Bound",
                "Upper Bound",
                "Generated At",
            ]
        )

        preds = (
            DemandPrediction.query.join(Medicine)
            .order_by(Medicine.name.asc(), DemandPrediction.forecast_date.asc())
            .all()
        )

        for p in preds:
            writer.writerow(
                [
                    p.medicine_id,
                    p.medicine.name if p.medicine else "Unknown",
                    p.forecast_date.strftime("%Y-%m-%d"),
                    p.horizon_days,
                    round(p.predicted_units, 2),
                    round(p.baseline_units, 2),
                    p.model_name,
                    round(p.mae, 3) if p.mae else "N/A",
                    round(p.rmse, 3) if p.rmse else "N/A",
                    round(p.confidence_lower, 2) if p.confidence_lower else "N/A",
                    round(p.confidence_upper, 2) if p.confidence_upper else "N/A",
                    p.created_at.strftime("%Y-%m-%d %H:%M"),
                ]
            )

        return output.getvalue()
