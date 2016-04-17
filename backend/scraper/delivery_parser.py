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
        merchant_db = parse_merchant(merchant)
        merchant_dbs.append(merchant_db.to_dict(include=MerchantModel.get_public_properties()))

    products = []
    for item_id in data.get('products'):
        item = data.get('products').get(item_id)
        item_db = parse_product(item)
        products.append(item_db.to_dict(include=ProductModel.get_public_properties()))

    return 200


def parse_merchant(merchant):
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
    return merchant_db


def parse_product(product, id=None):
    item_key = ndb.Key(ProductModel, id or product.get('product_id'))
    item_db = item_key.get()
    if not item_db:
        item_db = ProductModel(key=item_key)

    merchant_keys = []
    if 'merchant_id' in product:
        merchant_keys.append(str(product.get('merchant_id')))
    else:
        for id in product.get('merchant_ids'): # add all the merchant keys
            merchant_keys.append(str(id))

    brand = None
    #parse tags for breweries
    for tag in product.get('tags'):
        if "brand" == tag.get('key'):
            brand = tag.get('value')[0]

    if brand:
        merchant_key = ndb.Key(MerchantModel, brand)
        merchant_db = merchant_key.get()
        if not merchant_db:
            merchant_db = MerchantModel(
                key = merchant_key,
                name = brand
            )
            merchant_db.put()
        merchant_keys.append(brand)

    # create the product model
    item_db.populate(**dict(
        merchant_keys = merchant_keys,
        description = product.get('description'),
        size = product.get('size'),
        name = product.get('name'),
        image = product.get('image'),
        product_id = product.get('product_id'),
        tags = product.get('tags'),
        quantity = product.get('size_price')[0].get('quantity') if 'size_price' in product else 1,
        price = product.get('price')
    ))
    item_db.put()
    return item_db