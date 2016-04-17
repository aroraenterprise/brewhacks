"""
Project: backend
Author: Saj Arora
Description: 
"""
from google.appengine.ext import ndb

from api import make_list_response
from api.models import ProductModel, MerchantModel, BrandModel
from main import API
from flask_restful import Resource


@API.resource('/api/v1/brands')
class BrandsResource(Resource):
    def get(self):  # lists all the products
        brands = BrandModel.query().fetch()

        final_brands = []
        for brand in brands:
            results = [x.to_dict(ProductModel.get_public_properties()) for x in
                       ProductModel.query(ProductModel.brand_key == brand.key).fetch()]
            brand = brand.to_dict(include=BrandModel.get_public_properties())
            brand['products'] = results
            if len(results) > 0:
                final_brands.append(brand)
        return make_list_response(final_brands)

