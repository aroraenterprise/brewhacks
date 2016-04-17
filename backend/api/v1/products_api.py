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


@API.resource('/api/v1/products')
class ProductsResource(Resource):
    def get(self):  # lists all the products
        results = [x.to_dict(ProductModel.get_public_properties()) for x in
                       ProductModel.query().fetch()]
        return make_list_response(results)

