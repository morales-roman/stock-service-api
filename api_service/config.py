"""Default configuration

Use env var to override
"""
import os

ENV = os.getenv("FLASK_ENV")
DEBUG = ENV == "development"
SECRET_KEY = os.getenv("SECRET_KEY")

SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI")
SQLALCHEMY_TRACK_MODIFICATIONS = False

SERVICE_RUN_HOST = os.getenv("SERVICE_RUN_HOST")
SERVICE_RUN_PORT = os.getenv("SERVICE_RUN_PORT")
API_VERSION = "v1"

STOCK_SERVICE_URL = f"http://{SERVICE_RUN_HOST}:{SERVICE_RUN_PORT}/api/{API_VERSION}"
