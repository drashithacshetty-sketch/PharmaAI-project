import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


class Config:
    """Application configuration with environment variable loading."""

    SECRET_KEY = os.getenv(
        "SECRET_KEY", "medismart-ai-insecure-dev-secret-key-change-in-production"
    )

    # Database configuration
    USE_SQLITE = os.getenv("USE_SQLITE", "True").lower() in ("true", "1", "yes")

    MYSQL_USER = os.getenv("MYSQL_USER", "root")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
    MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
    MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")
    MYSQL_DB = os.getenv("MYSQL_DB", "medismart_db")

    explicit_db_uri = os.getenv("DATABASE_URL")

    if explicit_db_uri:
        SQLALCHEMY_DATABASE_URI = explicit_db_uri
    elif USE_SQLITE:
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{BASE_DIR / 'medismart.db'}"
    else:
        # MySQL connection string using PyMySQL driver
        pw_str = f":{MYSQL_PASSWORD}" if MYSQL_PASSWORD else ""
        SQLALCHEMY_DATABASE_URI = (
            f"mysql+pymysql://{MYSQL_USER}{pw_str}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}?charset=utf8mb4"
        )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_recycle": 280,
        "pool_pre_ping": True,
    }

    # Configurable Expiry Thresholds (Days)
    EXPIRY_CRITICAL_DAYS = int(os.getenv("EXPIRY_CRITICAL_DAYS", 7))
    EXPIRY_SOON_DAYS = int(os.getenv("EXPIRY_SOON_DAYS", 30))
    EXPIRY_WATCH_DAYS = int(os.getenv("EXPIRY_WATCH_DAYS", 90))

    # Reorder parameters
    DEFAULT_LEAD_TIME_DAYS = int(os.getenv("DEFAULT_LEAD_TIME_DAYS", 7))
    DEFAULT_HORIZON_DAYS = int(os.getenv("DEFAULT_HORIZON_DAYS", 30))
    DEFAULT_SERVICE_LEVEL_Z = float(os.getenv("DEFAULT_SERVICE_LEVEL_Z", 1.65))  # ~95% service level

    # ML & Data storage paths
    MODEL_DIR = BASE_DIR / os.getenv("MODEL_DIR", "ml/saved_models")
    DATA_PATH = BASE_DIR / os.getenv("DATA_PATH", "data/synthetic_sales.csv")


class TestingConfig(Config):
    """Configuration for automated test suite."""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False
