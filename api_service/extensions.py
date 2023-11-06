# encoding: utf-8

from flask_sqlalchemy import SQLAlchemy
from passlib.context import CryptContext
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate

from sqlalchemy.exc import IntegrityError
from datetime import datetime
from sqlalchemy.orm import joinedload as jl


db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
IError = IntegrityError
dt = datetime
joinedload = jl
