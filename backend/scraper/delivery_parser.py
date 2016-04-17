"""
Project: backend
Author: Saj Arora
Description: 
"""
from google.appengine.ext import ndb

from api import errors
from api.models import ProductModel, MerchantModel


def parse_delivery(data):
    # iterate over all the vendors
    if 'merchants' not in data:
        errors.create(500, message="No merchants found")
    merchants = data.get('merchants')

    merchant_dbs = []
    for merchant in merchants:
        # make this into a db model
        merchant_key = ndb.Key(MerchantModel, merchant.get('id'))
        merchant_db = merchant_key.get()
        if not merchant_db:
            merchant_db = MerchantModel(key=merchant_key)

        summary = merchant.get('summary')
        payment_types = []
        if summary.get('payment_types'):
            for payment in summary.get('payment_types'):
                payment_types.append(payment)

        merchant_db.populate(**dict(
            location = ('%s,%s' % (str(merchant.get('location').get('latitude')),
                                   str(merchant.get('location').get('longitude')))
                        ), # location.latitude, location.longitude
            #summary
            id = summary.get('id'),
            description = summary.get('description'),
            merchant_logo = summary.get('merchant_logo'),
            name = summary.get('name'),
            phone = summary.get('phone'),
            num_ratings = summary.get('num_ratings'),
            overall_ratings = summary.get('overall_ratings'),
            payment_types=payment_types
        ))
        merchant_db.put()
        merchant_dbs.append(merchant_db.to_dict(include=MerchantModel.get_public_properties()))

    products = []
    for item_id in data.get('products'):
        item = data.get('products').get(item_id)
        item_key = ndb.Key(ProductModel, item_id)
        item_db = item_key.get()

        if not item_db:
            item_db = ProductModel(key=item_key)

        merchant_keys = []
        for id in item.get('merchant_ids'): # add all the merchant keys
            merchant_keys.append(id)

        # create the product model
        item_db.populate(**dict(
            merchant_keys = merchant_keys,
            description = item.get('description'),
            size = item.get('size'),
            name = item.get('name'),
            image = item.get('image'),
            product_id = item.get('product_id'),
            tags = item.get('tags'),
            quantity = item.get('size_price')[0].get('quantity'),
            price = item.get('price')
        ))
        item_db.put()
        products.append(item_db.to_dict(include=ProductModel.get_public_properties()))

    return dict(merchants=merchant_dbs, products=products)