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
        """
        Retrieve stock data from the stooq service based on the stock code provided in the query parameter.

        Returns:
            A serialized representation of the stock data object.
        """
        
        stock_code = request.args.get('q')
        if not stock_code:
            return {'API Error': 'Missing stock code'}, 400  
        
        stooq_url = current_app.config['STOOQ_API_URL'].format(stock_code)
        stock_data_obj = requests.get(stooq_url)
        stock_data_obj.raise_for_status() 

        # Since the stooq API returns a list of objects, we only take the first one
        stock_data_obj = stock_data_obj.json()['symbols'][0]

        if not stock_data_obj.get('name'):
            return {'API Error': 'Invalid stock code'}, 400
        
        schema = StockSchema()
        
        return schema.dump(stock_data_obj)
