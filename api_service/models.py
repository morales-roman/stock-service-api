# encoding: utf-8

from sqlalchemy.ext.hybrid import hybrid_property
from api_service.extensions import db, pwd_context


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    _password = db.Column("password", db.String(255), nullable=False)
    active = db.Column(db.Boolean, default=True)
    role = db.Column(db.String(20), nullable=False)

    requests = db.relationship('RequestHistory', backref='user', lazy=True)


    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = pwd_context.hash(value)

    def __repr__(self):
        return "<User %s>" % self.username


class StockEntry(db.Model):
    __tablename__ = 'stock_entries'

    id = db.Column(db.Integer, primary_key=True)
    request_datetime = db.Column(db.DateTime, nullable=False)
    name = db.Column(db.String(64), nullable=False)
    symbol = db.Column(db.String(10), nullable=False)
    open = db.Column(db.Float, nullable=False)
    high = db.Column(db.Float, nullable=False)
    low = db.Column(db.Float, nullable=False)
    close = db.Column(db.Float, nullable=False)

    requests = db.relationship('RequestHistory', backref='stock_entry', lazy=True)

    def __repr__(self):
        return f'<StockEntry {self.name} ({self.symbol})>'
    
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class RequestHistory(db.Model):
    __tablename__ = 'requests_history'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    entries_id = db.Column(db.Integer, db.ForeignKey('stock_entries.id'), nullable=False)

    def __repr__(self):
        return f'<RequestHistory {self.user_id} requested {self.entries_id}>'

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class StockStat(db.Model):
    __tablename__ = 'stock_stats'

    id = db.Column(db.Integer, primary_key=True)
    stock_symbol = db.Column(db.String(10), nullable=False, unique=True)
    times_requested = db.Column(db.Integer, default=1)

    def __repr__(self):
        return f'<StockStat {self.stock_symbol} requested {self.times_requested} times>'

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

