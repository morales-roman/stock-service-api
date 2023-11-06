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
        
        self.save_data(data_from_service) # Save the response from the stock service
        reduced_data = self.reduce_data(data_from_service)
        
        schema = StockInfoSchema()

        return schema.dump(reduced_data)
    
    def reduce_data(self, data):
        return {
            'symbol': data['symbol'],
            'company_name': data['name'],
            'quote': data['close']
        }
    
    def save_data(self, data):
        user = User.query.filter_by(username=auth.current_user()).first()
        date_ = dt.strptime(data['date'], '%Y-%m-%d').date()
        time_= dt.strptime(data['time'], '%H:%M:%S').time()
        datetime_ = dt.combine(date_, time_)
        # Transaction to save the stock entry and the request history
        with db.session.begin_nested():
            stock_entry = StockEntry(
                name=data['name'],
                symbol=data['symbol'],
                open=data['open'],
                high=data['high'],
                low=data['low'],
                close=data['close'],
                request_datetime=datetime_
            )
            db.session.add(stock_entry)
            # Flush the session to get the ID of the new StockEntry
            db.session.flush()

            request = RequestHistory(
                user_id=user.id, 
                entries_id=stock_entry.id
            )
            db.session.add(request)

        # Commit the session to save the changes
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


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
        print("HERE STATS")
