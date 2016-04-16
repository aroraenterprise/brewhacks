"""
Project: backend
Author: Saj Arora
Description: 
"""
from google.appengine.ext import ndb

from api.models import Base


class TestModel(Base):
    name = ndb.StringProperty(required=True)
    place = ndb.StringProperty()

    PUBLIC_PROPERTIES = ['name', 'place']
