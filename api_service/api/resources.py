from flask import request, current_app
from flask_restful import Resource
import requests
from api_service.api.schemas import StockInfoSchema
from api_service.extensions import db
from api_service.models import User, StockEntry, RequestHistory, StockStat
from api_service.auth.helpers import auth, admin_required
from sqlalchemy.exc import IntegrityError
from datetime import datetime as dt

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
        reduced_data = self.reduce_data(data_from_service)
        
        schema = StockInfoSchema()

        return schema.dump(reduced_data)
    
    def reduce_data(self, data):
        return {
            'symbol': data['symbol'],
            'company_name': data['name'],
            'quote': data['close']
        }
    
    def save_data_to_db(self, data):
        user = User.query.filter_by(username=auth.current_user()).first()
        
        # Transaction to save the stock entry and the request history
        with db.session.begin_nested():
            stock_entry = self.arrange_stock_entry(data)
            db.session.add(stock_entry)
            db.session.flush() # Flush the session to get the ID of the new StockEntry
            request_history = self.arrange_request_history(user, stock_entry)
            db.session.add(request_history)
            self.add_or_merge_stock_stat(stock_entry.symbol)
            
        # Commit the session to save the changes
        try:
            db.session.commit()
        except IntegrityError:
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
        stock_stat = StockStat.query.filter_by(stock_symbol=stock_symbol).first()
        if stock_stat:
            stock_stat.times_requested += 1 # Increment the times requested
        else:
            stock_stat = StockStat(stock_symbol=stock_symbol)
            db.session.add(stock_stat)


class History(Resource):
    """
    Returns queries made by current user.
    """
    @auth.login_required
    def get(self):
        # TODO: Implement this method.
        pass


class Stats(Resource):
    """
    Allows admin users to see which are the most queried stocks.
    """
    @auth.login_required
    @admin_required
    def get(self):
        # TODO: Implement this method.
        pass
