"""
Project: backend
Author: Saj Arora
Description: 
"""
from google.appengine.ext import ndb

from api import make_list_response, make_empty_ok_response, errors
from api.models import ProductModel, MerchantModel
from main import API
from flask_restful import Resource

from flask_restful import reqparse


@API.resource('/api/v1/products/<string:pid>')
class ProductsIdResource(Resource):
    def get(self, pid):
        product_db = ProductModel.query(ProductModel.product_id == pid).get()
        if product_db:
            brewer_db = product_db.brand_key.get()
            response = product_db.to_dict(include=ProductModel.get_public_properties())
            response['brewer'] = brewer_db.name
            return response
        else:
            errors.create(404)

@API.resource('/api/v1/products')
class ProductsResource(Resource):
    def get(self):  # lists all the products
        # results = [{x.name: x.product_id} for x in
        #                ProductModel.query().fetch()]
        results = [x.to_dict(ProductModel.get_public_properties()) for x in
                       ProductModel.query().fetch()]
        return make_list_response(results)

    def delete(self):
        keys = ProductModel.query().fetch(keys_only=True)
        ndb.delete_multi(keys)
        return make_empty_ok_response()

