from flask import request, current_app
from flask_restful import Resource
import requests
from api_service.api.schemas import StockInfoSchema
from api_service.extensions import db
from api_service.models import User, StockEntry, RequestHistory, StockStat
from api_service.auth.helpers import auth, admin_required

class StockQuery(Resource):
    """
    Endpoint to allow users to query stocks
    """
    @auth.login_required
    def get(self):
        # TODO: Call the stock service, save the response, and return the response to the user in
        # the format dictated by the StockInfoSchema.
        stock_code = request.args.get('q')
        stock_service_url = current_app.config["STOCK_SERVICE_URL"]
        stock_service_endpoint = f"{stock_service_url}/stock"

        data_from_service = requests.get(stock_service_endpoint, params={'q': stock_code})
        if data_from_service.status_code != 200:
            return data_from_service.json(), data_from_service.status_code
        
        data_from_service = data_from_service.json()
        reduced_data = self.reduce_data(data_from_service)
        
        schema = StockInfoSchema()

        return schema.dump(reduced_data)
    
    def reduce_data(self, data):
        return {
            'symbol': data['symbol'],
            'company_name': data['name'],
            'quote': data['close']
        }


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
