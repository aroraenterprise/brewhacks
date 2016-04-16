"""
Project: backend
Author: Saj Arora
Description: 
"""
from datetime import date
from google.appengine.ext import ndb
import pydash as _


class Base(ndb.Expando):
    """Base model class, it should always be extended

    Attributes:
        created (ndb.DateTimeProperty): DateTime when model instance was created
        modified (ndb.DateTimeProperty): DateTime when model instance was last time modified
        version (ndb.IntegerProperty): Version of app

        PUBLIC_PROPERTIES (list): list of properties, which are accessible for public, meaning non-logged
            users. Every extending class should define public properties, if there are some
        PRIVATE_PROPERTIES (list): list of properties accessible by admin or authrorized user
    """
    created = ndb.DateTimeProperty(auto_now_add=True)
    modified = ndb.DateTimeProperty(auto_now=True)

    PUBLIC_PROPERTIES = ['key', 'version', 'created', 'modified']
    PRIVATE_PROPERTIES = []

    def to_dict(self, include=None):
        """Return a dict containing the entity's property values, so it can be passed to client

        Args:
            include (list, optional): Set of property names to include, default all properties
        """
        _MODEL = type(self)
        repr_dict = {}
        if include is None:
            return super(Base, self).to_dict(include=include)

        for name in include:
            #process name eg. email.private becomes email and include becomes private
            #include can be public, private
            try:
                name_array = name.split('.')
                processed_name = name_array[0]
                processed_include = name_array[1]
            except:
                processed_name = name
                processed_include = None

            # check if this property is even allowed to be public
            # or has a value set
            if not hasattr(self, processed_name):
                continue

            value = getattr(self, processed_name)
            if type(getattr(_MODEL, processed_name)) == ndb.StructuredProperty:
                if isinstance(value, list):
                    items = []
                    for item in value:
                        items.append(item.to_dict(include=item.get_private_properties()
                        if processed_include == 'private' else item.get_public_properties()))
                    repr_dict[processed_name] = items
                else:
                    repr_dict[processed_name] = value.to_dict(include=item.get_private_properties()
                        if processed_include == 'private' else item.get_public_properties())
            elif isinstance(value, date):
                repr_dict[processed_name] = value.isoformat()
            elif isinstance(value, ndb.Key):
                repr_dict[processed_name] = value.urlsafe()
            else:
                repr_dict[processed_name] = value

            repr_dict['id'] = self.get_id()
        return repr_dict

    def populate(self, **kwargs):
        """Extended ndb.Model populate method, so it can ignore properties, which are not
        defined in model class without throwing error
        """
        kwargs = _.omit(kwargs, Base.PUBLIC_PROPERTIES + ['key', 'id'])  # We don't want to populate those properties
        kwargs = _.pick(kwargs, _.keys(self._properties))  # We want to populate only real model properties
        super(Base, self).populate(**kwargs)

    @classmethod
    def get_by(cls, name, value, keys_only=None):
        """Gets model instance by given property name and value
        :param name:
        :param value:
        :param keys_only:
        """
        return cls.query(getattr(cls, name) == value).get(keys_only=keys_only)

    @classmethod
    def fetch_by(cls, name, value, keys_only=None, cursor=None, limit=None):
        """Gets model instance by given property name and value
        :param name:
        :param value:
        :param keys_only:
        :param cursor:
        :param limit:
        """
        return cls.query(getattr(cls, name) == value)\
            .fetch(keys_only=keys_only, cursor=cursor, limit=limit)

    @classmethod
    def get_public_properties(cls):
        """Public properties consist of this class public properties
        plus extending class public properties"""
        return cls.PUBLIC_PROPERTIES + Base.PUBLIC_PROPERTIES

    @classmethod
    def get_private_properties(cls):
        """Gets private properties defined by extending class"""
        public_properties = cls.get_public_properties()
        for item in cls.PRIVATE_PROPERTIES:
            try:
                name = item.split('.')
                public_properties.remove(name[0]) #private overrides public
            except:
                pass

        props = cls.PRIVATE_PROPERTIES + Base.PRIVATE_PROPERTIES + public_properties
        return props

    @classmethod
    def get_all_properties(cls):
        """Gets all model's ndb properties"""
        return ['key', 'id'] + _.keys(cls._properties)

    def get_id(self):
        return self.key.id()


    def get_key(self):
        return self.key.urlsafe()


    @classmethod
    def is_valid(self, model):
        return True, {}

    def get_rsvp_message(self):
        return None # default none

    def get_name(self):
        if hasattr(self, 'name'):
            return self.name
        else:
            return type(self).__name__