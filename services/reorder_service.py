from datetime import date, timedelta
import math
from typing import List, Dict, Any
import numpy as np
from models import (
    Medicine,
    DailyMedicineSales,
    DemandPrediction,
    PurchaseOrder,
    PurchaseOrderItem,
)


class ReorderService:
    """
    Intelligent inventory replenishment engine using statistical safety stock,
    supplier lead time demand, and AI forecast projections.
    """

    @staticmethod
    def calculate_recommendation(
        medicine: Medicine,
        horizon_days: int = 30,
        service_level_z: float = 1.65,
        lead_time_override: int | None = None,
    ) -> Dict[str, Any]:
        """
        Calculate smart replenishment metrics for a single medicine:
        - Lead time demand (LTD)
        - Safety stock (SS)
        - Reorder point (ROP)
        - Target stock level
        - Usable on-hand stock
        - Incoming purchase orders
        - Pack-size adjusted recommended order quantity
        """
        # Determine supplier lead time
        if lead_time_override is not None and lead_time_override > 0:
            lead_time = lead_time_override
        elif medicine.preferred_supplier and medicine.preferred_supplier.lead_time_days > 0:
            lead_time = medicine.preferred_supplier.lead_time_days
        else:
            lead_time = 7  # Standard default lead time

        # 1. Fetch recent sales history (past 30 days) to compute demand statistics
        cutoff_date = date.today() - timedelta(days=30)
        recent_sales = (
            DailyMedicineSales.query.filter(
                DailyMedicineSales.medicine_id == medicine.id,
                DailyMedicineSales.sale_date >= cutoff_date,
            )
            .order_by(DailyMedicineSales.sale_date.asc())
            .all()
        )

        daily_units = [s.total_units_sold for s in recent_sales]
        if daily_units:
            # Pad with 0 for missing dates within the 30-day window
            total_days_logged = len(daily_units)
            if total_days_logged < 30:
                daily_units.extend([0] * (30 - total_days_logged))
            avg_daily_demand = float(np.mean(daily_units))
            std_daily_demand = float(np.std(daily_units))
        else:
            # Fallback when no daily records exist
            avg_daily_demand = max(1.0, float(medicine.reorder_level) / 30.0)
            std_daily_demand = avg_daily_demand * 0.4

        # Check for latest ML forecast projection if available
        latest_pred = (
            DemandPrediction.query.filter_by(medicine_id=medicine.id)
            .order_by(DemandPrediction.created_at.desc())
            .first()
        )
        if latest_pred and latest_pred.predicted_units > 0:
            # Blend ML forecast with recent mean: 70% ML forecast daily rate, 30% recent empirical mean
            ml_daily_rate = float(latest_pred.predicted_units) / float(latest_pred.horizon_days)
            blended_daily_demand = (ml_daily_rate * 0.70) + (avg_daily_demand * 0.30)
            demand_source = f"AI Hybrid ({latest_pred.model_name})"
        else:
            blended_daily_demand = avg_daily_demand
            demand_source = "Empirical 30-day Average"

        daily_demand = max(0.5, blended_daily_demand)

        # 2. Safety Stock Formula: SS = Z * sigma_d * sqrt(LeadTime)
        # Accounts for demand variability during supplier replenishment latency
        if std_daily_demand > 0.05:
            safety_stock = service_level_z * std_daily_demand * math.sqrt(lead_time)
        else:
            # Minimum baseline buffer
            safety_stock = daily_demand * 2.0
        safety_stock = math.ceil(safety_stock)

        # 3. Lead Time Demand: LTD = daily_demand * lead_time
        lead_time_demand = math.ceil(daily_demand * lead_time)

        # 4. Reorder Point: ROP = LTD + SS
        # If usable stock drops to or below ROP, an order must be placed immediately
        reorder_point = lead_time_demand + safety_stock

        # 5. Target Stock Level for the Planning Horizon (e.g. 30 days)
        target_stock = math.ceil((daily_demand * horizon_days) + safety_stock)

        # 6. Inventory Positions
        usable_stock = medicine.usable_stock

        # Calculate incoming orders: approved/active POs not yet received
        incoming_items = (
            PurchaseOrderItem.query.join(PurchaseOrder)
            .filter(
                PurchaseOrderItem.medicine_id == medicine.id,
                PurchaseOrder.status.in_(["Draft", "Ordered"]),
            )
            .all()
        )
        incoming_stock = sum(
            item.requested_quantity - item.received_quantity for item in incoming_items
        )

        net_inventory_position = usable_stock + incoming_stock

        # 7. Check if reorder trigger is met
        needs_reorder = (
            net_inventory_position <= reorder_point
            or usable_stock <= medicine.reorder_level
        )

        # 8. Calculate order quantity rounded up to supplier pack size
        pack_size = max(1, medicine.pack_size)
        raw_deficit = max(0, target_stock - net_inventory_position)

        if needs_reorder and raw_deficit > 0:
            recommended_packs = math.ceil(raw_deficit / pack_size)
            recommended_units = recommended_packs * pack_size
        else:
            recommended_packs = 0
            recommended_units = 0

        # Estimated stockout days remaining
        days_of_stock = (
            round(usable_stock / daily_demand, 1) if daily_demand > 0 else 999.0
        )

        # Urgency assessment
        if usable_stock <= 0:
            urgency = "CRITICAL_STOCKOUT"
            review_flag = "OUT OF STOCK: Immediate order required to prevent lost sales."
        elif usable_stock < lead_time_demand:
            urgency = "HIGH_RISK"
            review_flag = f"STOCKOUT IMMINENT: Stock will run out before supplier lead time ({lead_time} days)."
        elif needs_reorder:
            urgency = "REORDER_TRIGGERED"
            review_flag = "Reorder point reached. Standard purchase order recommended."
        else:
            urgency = "HEALTHY"
            review_flag = "Stock is currently sufficient for planning horizon."

        estimated_unit_cost = (
            medicine.default_selling_price * 0.7 if medicine.default_selling_price > 0 else 25.0
        )
        estimated_order_cost = round(recommended_units * estimated_unit_cost, 2)

        return {
            "medicine_id": medicine.id,
            "medicine_name": medicine.name,
            "generic_name": medicine.generic_name,
            "category": medicine.category,
            "unit": medicine.unit,
            "pack_size": pack_size,
            "supplier_name": (
                medicine.preferred_supplier.name
                if medicine.preferred_supplier
                else "Unassigned"
            ),
            "lead_time_days": lead_time,
            "predicted_daily_demand": round(daily_demand, 2),
            "demand_std_dev": round(std_daily_demand, 2),
            "demand_source": demand_source,
            "lead_time_demand": lead_time_demand,
            "safety_stock": safety_stock,
            "reorder_point": reorder_point,
            "target_stock": target_stock,
            "usable_stock": usable_stock,
            "incoming_stock": incoming_stock,
            "net_inventory_position": net_inventory_position,
            "days_of_stock": days_of_stock,
            "needs_reorder": needs_reorder,
            "recommended_packs": recommended_packs,
            "recommended_units": recommended_units,
            "estimated_order_cost": estimated_order_cost,
            "urgency": urgency,
            "review_flag": review_flag,
        }

    @staticmethod
    def get_all_reorder_recommendations(
        horizon_days: int = 30, only_needed: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Calculate reorder recommendations for all active medicines in catalog.
        Sorted by urgency: CRITICAL first, then HIGH_RISK, then REORDER_TRIGGERED.
        """
        medicines = Medicine.query.filter_by(is_active=True).all()
        recommendations = [
            ReorderService.calculate_recommendation(m, horizon_days=horizon_days)
            for m in medicines
        ]

        if only_needed:
            recommendations = [r for r in recommendations if r["needs_reorder"]]

        # Sort order priority: CRITICAL -> HIGH_RISK -> REORDER_TRIGGERED -> HEALTHY
        urgency_rank = {
            "CRITICAL_STOCKOUT": 0,
            "HIGH_RISK": 1,
            "REORDER_TRIGGERED": 2,
            "HEALTHY": 3,
        }
        recommendations.sort(
            key=lambda r: (urgency_rank.get(r["urgency"], 99), r["days_of_stock"])
        )
        return recommendations
