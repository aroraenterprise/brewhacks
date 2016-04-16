"""
Project: backend
Author: Saj Arora
Description: 
"""
from google.appengine.ext import ndb

from api.models import Base

class ProductModel(Base):
    merchant_keys = ndb.IntegerProperty(repeated=True)
    description = ndb.StringProperty()
    size = ndb.StringProperty()
    name = ndb.StringProperty()
    image = ndb.StringProperty()
    product_id = ndb.StringProperty()
    tags = ndb.JsonProperty(repeated=True)
    quantity = ndb.IntegerProperty(required=True)
    price = ndb.FloatProperty(required=True)
    unit_price = ndb.ComputedProperty(lambda x: x.price/x.quantity)

    PUBLIC_PROPERTIES = ['merchant_keys', 'description', 'size', 'name',
                         'image', 'product_id', 'tags', 'quantity',
                         'price', 'unit_price']
