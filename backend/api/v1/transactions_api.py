"""
Project: backend
Author: Saj Arora
Description: 
"""
import json
import urllib

from flask import request
from google.appengine.api import urlfetch
from google.appengine.ext import ndb

import scraper
from api import make_list_response, make_empty_ok_response, errors
from api.models import ProductModel, MerchantModel, TransactionModel
from main import API
from flask_restful import Resource
import pydash as _

from flask_restful import reqparse


@API.resource('/api/v1/transactions')
class TransactionsResource(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('product_id', required=True)
        args = parser.parse_args()

        # return ndb.Key(ProductModel, args.get('product_id')).get().to_dict(include=ProductModel.get_public_properties())

        items = [x.to_dict(include=TransactionModel.get_public_properties()) for x in
                 TransactionModel.query(TransactionModel.product_key==
                                        ndb.Key(ProductModel, args.get('product_id'))).fetch()]
        return make_list_response(items)

    def post(self): # lists all the products
        args = _.pick(request.json, TransactionModel.PUBLIC_PROPERTIES + ['merchant_id', 'product_id'])

        merchant_db = product_db = None
        if args.get('merchant_id'): # do a look up
            url = "https://www.delivery.com/api/merchant/%s?client_id=brewhacks2016" % args.get('merchant_id')
            result = urlfetch.fetch(url)
            if result.status_code == 200:
                data = json.loads(result.content)
                merchant_db = scraper.parse_merchant(data.get('merchant'))
                args['merchant_key'] = merchant_db._key
        else:
            args['merchant_key'] = ndb.Key(urlsafe=args.get('merchant_key'))
            merchant_db = args.get('merchant_key').get()

        if not merchant_db: # look it up
            errors.create(404, message="merchant not found")

        # do products
        if args.get('product_id'): # do a look up
            url = "https://www.delivery.com/api/data/product/%(product)s?merchant_id=%(merchant)s" \
                  "&client_id=brewhacks2016" % dict(product=args.get('product_id'),
                                                    merchant=args.get('merchant_id'))
            result = urlfetch.fetch(url)
            if result.status_code == 200:
                data = json.loads(result.content)
                product_db = scraper.parse_product(data.get('item')[0], data.get('item')[0].get('id'))
                args['product_key'] = product_db._key
        else:
            args['product_key'] = ndb.Key(urlsafe=args.get('product_key'))
            product_db = args.get('product_key').get()

        if not product_db: # look it up
            errors.create(404, message="product not found")

        args['merchant'] = merchant_db
        args['product'] = product_db

        transaction_db = TransactionModel(**args)
        transaction_db.put()
        return transaction_db.to_dict(include=TransactionModel.get_public_properties())

    def delete(self):
        keys = TransactionModel.query().fetch(keys_only=True)
        ndb.delete_multi(keys)
        return make_empty_ok_response()