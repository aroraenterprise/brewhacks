"""
Project: backend
Author: Saj Arora
Description: 
"""
from google.appengine.ext import ndb

from api.models import Base, MerchantModel


class ProductModel(Base):
    merchant = ndb.StructuredProperty(MerchantModel, repeated=True)
    brand_key = ndb.KeyProperty()
    description = ndb.TextProperty()
    size = ndb.StringProperty()
    name = ndb.StringProperty()
    image = ndb.StringProperty()
    product_id = ndb.StringProperty()
    tags = ndb.JsonProperty(repeated=True)
    quantity = ndb.IntegerProperty(required=True)
    price = ndb.FloatProperty(required=True)
    unit_price = ndb.ComputedProperty(lambda x: x.price/x.quantity)

    PUBLIC_PROPERTIES = ['merchant', 'brand_key', 'description', 'size', 'name',
                         'image', 'product_id', 'tags', 'quantity',
                         'price', 'unit_price']
