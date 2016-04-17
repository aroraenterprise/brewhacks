"""
Project: backend
Author: Saj Arora
Description: 
"""
from google.appengine.ext import ndb

from api import make_list_response
from api.models import ProductModel, MerchantModel
from main import API
from flask_restful import Resource


@API.resource('/api/v1/merchants')
class MerchantsResource(Resource):
    def get(self):  # lists all the products
        merchants = [x.to_dict(include=MerchantModel.get_public_properties())
                     for x in MerchantModel.query().fetch()]

        for merchant in merchants:
            results = [x.to_dict(ProductModel.get_public_properties()) for x in
                       ProductModel.query(ProductModel.merchant_keys == int(merchant.get('id'))).fetch()]
            merchant['products'] = results
        return make_list_response(merchants)

