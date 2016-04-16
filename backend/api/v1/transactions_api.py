"""
Project: backend
Author: Saj Arora
Description: 
"""
from flask import request
from google.appengine.ext import ndb

from api import make_list_response, make_empty_ok_response, errors
from api.models import ProductModel, MerchantModel, TransactionModel
from main import API
from flask_restful import Resource
import pydash as _


@API.resource('/api/v1/transactions')
class TransactionsResource(Resource):
    def get(self):
        items = [x.to_dict(include=TransactionModel.get_public_properties()) for x in TransactionModel.query().fetch()]
        return make_list_response(items)

    def post(self): # lists all the products
        args = _.pick(request.json, TransactionModel.PUBLIC_PROPERTIES)

        args['merchant_key'] = ndb.Key(urlsafe=args.get('merchant_key'))
        merchant_db = args.get('merchant_key').get()
        if not merchant_db:
            errors.create(404, message="merchant not found")

        args['product_key'] = ndb.Key(urlsafe=args.get('product_key'))
        product_db = args.get('product_key').get()
        if not product_db:
            errors.create(404, message="product not found")

        args['merchant'] = merchant_db
        args['product'] = product_db

        transaction_db = TransactionModel(**args)
        transaction_db.put()
        return transaction_db.to_dict(include=TransactionModel.get_public_properties())