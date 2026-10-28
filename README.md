# 🏥 PharmaAI — Smart Pharmacy Inventory & Demand Forecasting System

**PharmaAI** is a production-grade, AI-powered pharmacy inventory and supply chain management web application built with **Flask, SQLAlchemy, Bootstrap 5, and Scikit-Learn**. It features automated **First-Expiry, First-Out (FEFO)** batch allocation, multi-tier expiration alerting, dynamic safety stock reordering, and a machine learning demand forecasting engine to prevent both costly stockouts and drug wastage.

---

## 🌟 Key Features

### 1. 🛡️ First-Expiry, First-Out (FEFO) Engine
* **Strict Priority Queue**: Medicines are automatically allocated and sold from the earliest-expiring active batch first.
* **Expiry Risk Tiers**:
  * 🔴 **Critical Expiry**: ≤ 7 days remaining (prominent alert banners, disposal action available).
  * 🟡 **Expiring Soon**: ≤ 30 days remaining (priority sale queue).
  * 🟢 **Normal**: > 30 days remaining.
  * ⛔ **Expired**: Automatically blocked from dispensing and flagged for safe disposal.
* **Immutable Audit Trail**: Every stock addition, POS sale, PO receipt, and expired discard is logged with user attribution and timestamp.

### 2. 🤖 Machine Learning Demand Forecasting
* **Random Forest Regressor** trained on 400+ days of historical medicine sales.
* **Feature Engineering Without Data Leakage**: Rolling 7-day and 14-day demand averages, day-of-week, seasonality, and lag variables.
* **Multi-Horizon Projections**: 7-day and 30-day ahead forecasts with confidence bounds and Mean Absolute Error (MAE) benchmarks against baseline moving averages.

### 3. 📦 Smart Reorder & Procurement
* **Automated Reorder Point (ROP)**: Calculated based on lead time demand plus dynamic safety stock.
* **Suggested Order Quantities**: Recommends batch replenishment quantities aligned with supplier minimum pack sizes.
* **Purchase Order Lifecycle**: Create, review, approve, and receive multi-item supplier POs with automated inventory crediting.

### 4. 💳 POS Billing & Sales
* Fast dispensing interface with real-time stock validation, batch breakdown, and instant invoice generation.
* Role-based access control (Admin, Pharmacist, Staff).

### 5. 📊 Analytics & Reporting
* Real-time dashboard KPI cards (Usable Stock, Expiring Units, Monthly Revenue, Pending POs).
* Exportable CSV reports for Inventory, Sales History, Expiration Audits, and AI Demand Predictions.

---

## 🚀 Quick Start Guide

### Prerequisites
* Python 3.10+ (Python 3.11 recommended)
* Virtual environment (`.venv`)

### 1. Environment Setup
Activate the virtual environment and install dependencies:
```bash
# Windows PowerShell
.\.venv\Scripts\Activate.ps1

# Or install dependencies if setting up fresh
pip install -r requirements.txt
```

### 2. Database Initialization & Seeding
Initialize the database schema, seed test users, suppliers, product catalog, multi-tier batches, 400 days of synthetic sales history, and train the ML model:
```bash
python seed.py
```

### 3. Run the Development Server
```bash
python app.py
```
Open your browser at **`http://127.0.0.1:5000`**.

---

## 🔐 Default User Accounts

| Role | Username | Password | Access Level |
| :--- | :--- | :--- | :--- |
| **Administrator** | `admin` | `admin123` | Full access to all modules, users, PO approval, and reports |
| **Pharmacist** | `pharmacist` | `pharm123` | Inventory management, batch creation, dispensing, reordering |
| **Staff** | `staff` | `staff123` | POS billing, stock inquiry, customer sales receipts |

---

## 🧪 Automated Testing

PharmaAI includes a complete test suite covering inventory mechanics, FEFO logic, ML forecaster stability, and reordering calculations:
```bash
pytest
```
*Current test suite: **12 / 12 passing**.*

---

## 📂 Project Architecture

```
medismart-ai/
├── app.py                      # Flask application factory and blueprints registration
├── config.py                   # Environment-driven application settings
├── seed.py                     # Schema setup, demo data seeding, and initial ML training
├── requirements.txt            # Python dependencies
├── models/                     # SQLAlchemy ORM models (User, Medicine, Batch, Sale, PO, etc.)
├── services/                   # Business logic (InventoryService, SalesService, ReorderService)
├── ml/                         # Machine learning forecaster & feature engineering
│   ├── model.py                # DemandForecaster wrapper (Random Forest Regressor)
│   ├── feature_engineering.py  # Lag features, rolling statistics, seasonality
│   └── data_generator.py       # Realistic synthetic pharmacy sales generator
├── routes/                     # Blueprint controllers (Auth, Medicines, Batches, Sales, PO, Expiry, Forecast)
├── templates/                  # Jinja2 templates styled with Bootstrap 5 and modern UI tokens
│   ├── base.html               # Main responsive layout with dynamic alert badges
│   ├── dashboard/              # Executive KPI dashboard & quick actions
│   ├── medicines/              # Catalog and FEFO batch inspection views
│   ├── batches/                # Multi-batch registration and management
│   ├── expiry/                 # Expiration risk watchlist and safe disposal
│   ├── forecast/               # AI prediction charts and model metrics
│   ├── reorder/                # Smart procurement recommendations
│   ├── sales/                  # POS billing and invoice history
│   ├── purchase_orders/        # Supplier purchase order lifecycle
│   └── reports/                # Management analytics and CSV exports
├── static/                     # CSS stylesheets, JavaScript helpers, and custom UI components
└── tests/                      # Automated unit and integration test suite
```
