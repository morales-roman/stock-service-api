# encoding: utf-8

from flask import request, current_app
from flask_restful import Resource
import requests

from stock_service.api.schemas import StockSchema


class StockResource(Resource):
    """
    Endpoint that is in charge of aggregating the stock information from external sources and returning
    them to our main API service. Currently we only get the data from a single external source:
    the stooq API.
    """
    def get(self):        
        stock_code = request.args.get('q')
        if not stock_code:
            return {"API Error": "Missing stock code"}, 404
        
        stock_data_obj = self.get_stock_data(stock_code)
        if stock_data_obj.status_code != 200:
            return {"API Error": "The external API may be out of service"}, 502

        try:
            valid_stock_code, stock_data_obj = self.validate_stock_code(stock_data_obj)
        except Exception as e:
            return {"API Error": "The external API response is malformed."}, 502
        
        if not valid_stock_code:
            return stock_data_obj, 400
        
        schema = StockSchema()
        
        return schema.dump(stock_data_obj)

    def get_stock_data(self, stock_code):
        """
        Gets the stock data from the stooq API
        """
        stooq_url = current_app.config['STOOQ_API_URL'].format(stock_code)
        stock_data_obj = requests.get(stooq_url)
        return stock_data_obj

    def validate_stock_code(self, stock_data_obj):
        """
        Validates that the stock code is valid
        """
        stock_data_obj = stock_data_obj.json()['symbols'][0] # Get the first element of the list
        if not stock_data_obj.get('name'):
            return False, {"API Error": "Invalid stock code"}
        return True, stock_data_obj
