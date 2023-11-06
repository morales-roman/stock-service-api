# encoding: utf-8

from api_service.extensions import ma


class StockInfoSchema(ma.Schema):
    symbol = ma.String(dump_only=True)
    name = ma.String(dump_only=True, data_key='company_name')
    close = ma.Float(dump_only=True, data_key='quote')

class StockStatsSchema(ma.Schema):
    stock_symbol = ma.String(dump_only=True, data_key='stock')
    times_requested = ma.Integer(dump_only=True)

class HistorySchema(ma.Schema):
    request_datetime = ma.DateTime(dump_only=True,  data_key='date')
    name = ma.String(dump_only=True)
    symbol = ma.String(dump_only=True)
    open = ma.Float(dump_only=True)
    high = ma.Float(dump_only=True)
    low = ma.Float(dump_only=True)
    close = ma.Float(dump_only=True)

