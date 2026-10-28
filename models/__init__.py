from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user import User
from .supplier import Supplier
from .medicine import Medicine
from .batch import Batch
from .sale import Sale, SaleItem
from .stock_movement import StockMovement
from .purchase_order import PurchaseOrder, PurchaseOrderItem
from .daily_sales import DailyMedicineSales
from .demand_prediction import DemandPrediction

__all__ = [
    "db",
    "User",
    "Supplier",
    "Medicine",
    "Batch",
    "Sale",
    "SaleItem",
    "StockMovement",
    "PurchaseOrder",
    "PurchaseOrderItem",
    "DailyMedicineSales",
    "DemandPrediction",
]
