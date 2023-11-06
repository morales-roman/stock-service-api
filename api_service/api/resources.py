from flask import request, current_app
from flask_restful import Resource
import requests
from api_service.api.schemas import StockInfoSchema, StockStatsSchema, HistorySchema
from api_service.extensions import db, dt, IError
from api_service.models import User, StockEntry, RequestHistory, StockStat
from api_service.auth.helpers import auth, admin_required


class StockQuery(Resource):
    """
    Endpoint to allow users to query stocks
    """
    @auth.login_required
    def get(self):
        stock_code = request.args.get('q')
        stock_service_url = current_app.config["STOCK_SERVICE_URL"]
        stock_service_endpoint = f"{stock_service_url}/stock"

        data_from_service = requests.get(stock_service_endpoint, params={'q': stock_code})
        if data_from_service.status_code != 200:
            return data_from_service.json(), data_from_service.status_code
        
        data_from_service = data_from_service.json()
        self.save_data_to_db(data_from_service) # Save the response from the stock service
        schema = StockInfoSchema()

        return schema.dump(data_from_service)
    
    def save_data_to_db(self, data):
        user = User.query.filter_by(username=auth.current_user()).first()
        
        # Transaction to save the stock entry and the request history
        with db.session.begin_nested():
            # Save the stock entry
            stock_entry = self.arrange_stock_entry(data)
            db.session.add(stock_entry)
            # Flush the session to get the ID of the new StockEntry
            db.session.flush()
            # Save the request history
            request_history = self.arrange_request_history(user, stock_entry)
            db.session.add(request_history)
            # Add or update the stock stats
            self.add_or_merge_stock_stat(stock_entry.symbol)
            
        # Commit the session to save the changes
        try:
            db.session.commit()
        except IError:
            db.session.rollback()

    def arrange_stock_entry(self, data):
        date_ = dt.strptime(data['date'], '%Y-%m-%d').date()
        time_= dt.strptime(data['time'], '%H:%M:%S').time()
        datetime_ = dt.combine(date_, time_)
        stock_entry = StockEntry(
                name=data['name'],
                symbol=data['symbol'],
                open=data['open'],
                high=data['high'],
                low=data['low'],
                close=data['close'],
                request_datetime=datetime_
            )
        return stock_entry
    
    def arrange_request_history(self, user, stock_entry):
        request_history = RequestHistory(
                user_id=user.id,
                entries_id=stock_entry.id
            )
        return request_history
    
    def add_or_merge_stock_stat(self, stock_symbol):
        # If the stock symbol is already in the database, increment the times requested
        stock_stat = StockStat.query.filter_by(stock_symbol=stock_symbol).first()
        if stock_stat:
            stock_stat.times_requested += 1 
        else:
            # If the stock symbol is not in the database, add it
            stock_stat = StockStat(stock_symbol=stock_symbol)
            db.session.add(stock_stat)


class History(Resource):
    """
    Returns queries made by current user.
    """
    @auth.login_required
    def get(self):
        schema=HistorySchema(many=True)
        user = User.query\
            .filter_by(username=auth.current_user())\
            .first()

        # Get the stock entry requests made by the user
        requests = StockEntry.query\
            .join(RequestHistory, RequestHistory.entries_id == StockEntry.id)\
            .filter(RequestHistory.user_id == user.id)\
            .order_by(StockEntry.request_datetime.desc())\
            .all()
        return schema.dump(requests)

class Stats(Resource):
    """
    Allows admin users to see which are the most queried stocks.
    """
    @auth.login_required
    @admin_required
    def get(self):
        schema = StockStatsSchema(many=True)
        stock_stats = StockStat.query\
            .order_by(StockStat.times_requested.desc())\
            .limit(5)\
            .all()

        return schema.dump(stock_stats)