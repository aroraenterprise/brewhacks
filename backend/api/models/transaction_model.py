"""
Project: backend
Author: Saj Arora
Description: 
"""
from google.appengine.ext import ndb

from api.models import Base, ProductModel, MerchantModel


class TransactionModel(Base):
    email = ndb.StringProperty(required=True)
    gender = ndb.StringProperty()
    profile = ndb.StringProperty()
    age_group = ndb.StringProperty()
    job = ndb.StringProperty()

    product_key = ndb.KeyProperty(required=True)
    product = ndb.StructuredProperty(ProductModel)
    merchant_key = ndb.KeyProperty(required=True)
    merchant = ndb.StructuredProperty(MerchantModel)
    location = ndb.StringProperty()
    timestamp = ndb.StringProperty()

    PUBLIC_PROPERTIES = ['email', 'gender', 'profile', 'age_group',
                         'job', 'product_key', 'merchant_key', 'product',
                         'merchant', 'location', 'timestamp']