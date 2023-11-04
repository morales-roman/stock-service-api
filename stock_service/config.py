"""Default configuration

Use env var to override
"""
import os

ENV = os.getenv("FLASK_ENV")
DEBUG = ENV == "development"
SECRET_KEY = os.getenv("SECRET_KEY")
STOOQ_API_URL = os.getenv("STOOQ_API_URL")