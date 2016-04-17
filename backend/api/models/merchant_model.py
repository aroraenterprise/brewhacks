"""
Project: backend
Author: Saj Arora
Description: 
"""
from google.appengine.ext import ndb

from api.models import Base

class MerchantModel(Base):
    location = ndb.StringProperty() # location.latitude, location.longitude
    #summary
    description = ndb.TextProperty()
    merchant_logo = ndb.StringProperty()
    name = ndb.StringProperty()
    phone = ndb.StringProperty()
    num_ratings = ndb.IntegerProperty()
    overall_ratings = ndb.IntegerProperty()
    temp_key = ndb.KeyProperty()

    PUBLIC_PROPERTIES = ['products', 'location', 'description', 'merchant_logo',
                         'name', 'phone', 'num_ratings', 'overall_ratings', 'temp_key']
