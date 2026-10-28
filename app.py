import os
from flask import Flask, render_template
from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config
from models import db, User, Medicine, Batch
from services.inventory_service import InventoryService


login_manager = LoginManager()
migrate = Migrate()


def create_app(config_class=Config) -> Flask:
    """Application factory for PharmaAI."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please sign in to access the pharmacy management system."
    login_manager.login_message_category = "warning"

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register Blueprints
    from routes.main_routes import main_bp
    from routes.auth_routes import auth_bp
    from routes.medicine_routes import medicine_bp
    from routes.batch_routes import batch_bp
    from routes.sales_routes import sales_bp
    from routes.supplier_routes import supplier_bp
    from routes.po_routes import po_bp
    from routes.expiry_routes import expiry_bp
    from routes.forecast_routes import forecast_bp
    from routes.reorder_routes import reorder_bp
    from routes.report_routes import report_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(medicine_bp, url_prefix="/medicines")
    app.register_blueprint(batch_bp, url_prefix="/batches")
    app.register_blueprint(sales_bp, url_prefix="/sales")
    app.register_blueprint(supplier_bp, url_prefix="/suppliers")
    app.register_blueprint(po_bp, url_prefix="/purchase-orders")
    app.register_blueprint(expiry_bp, url_prefix="/expiry")
    app.register_blueprint(forecast_bp, url_prefix="/forecast")
    app.register_blueprint(reorder_bp, url_prefix="/reorder")
    app.register_blueprint(report_bp, url_prefix="/reports")

    # Global context processor for alerts badge counters in navbar
    @app.context_processor
    def inject_global_metrics():
        try:
            buckets = InventoryService.get_expiry_buckets(critical_days=7, soon_days=30)
            low_stock_count = Medicine.query.filter(Medicine.is_active == True).all()
            low_count = sum(1 for m in low_stock_count if m.is_low_stock)
            return {
                "critical_expiry_count": buckets["counts"]["critical"] + buckets["counts"]["expired"],
                "low_stock_count": low_count,
                "app_name": "PharmaAI",
                "app_version": "2.0.0",
            }
        except Exception:
            return {
                "critical_expiry_count": 0,
                "low_stock_count": 0,
                "app_name": "PharmaAI",
                "app_version": "2.0.0",
            }

    # Error handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template("errors/500.html"), 500

    return app


if __name__ == "__main__":
    application = create_app()
    with application.app_context():
        db.create_all()
    application.run(host="127.0.0.1", port=5000, debug=True)
