"""
Project: backend
Author: Saj Arora
Description: 
"""
import random

from google.appengine.ext import ndb

from api import make_list_response
from api.models import ProductModel, MerchantModel
from main import API
from flask_restful import Resource


@API.resource('/api/v1/merchants')
class MerchantsResource(Resource):
    def get(self):  # lists all the products
        merchants = [x.to_dict(include=MerchantModel.get_public_properties())
                     for x in MerchantModel.query().fetch()]

        final_merchants = []
        for merchant in merchants:
            results = [x.to_dict(ProductModel.get_public_properties()) for x in
                       ProductModel.query(ProductModel.merchant_keys == merchant.get('id')).fetch()]
            merchant['products'] = results
            if len(results) > 0:
                final_merchants.append(merchant)

        return make_list_response(final_merchants)

    def post(self):
        merchants = [
            MerchantModel(name='Taproom New York on third avenue',
                          location='38 W 56th St New York, NY 10019',
                          merchant_logo='http://s3-media2.fl.yelpcdn.com/bphoto/fqPnLDlIwm4Rq1kvESOgEg/90s.jpg',
                          num_ratings=100,
                          overall_rating=4.5),
            MerchantModel(name='Judge Roy Bean Public House',
                          location='1609 2nd Ave New York, NY 10028',
                          num_ratings=300,
                          overall_rating=3.8,
                          merchant_logo='http://s3-media3.fl.yelpcdn.com/bphoto/OwBC1Fgwt-Zk5bN3WBJwGw/90s.jpg'),
            MerchantModel(name='Jimmy\'s Corner',
                          num_ratings=150,
                          overall_rating=2.5,
                          location='140 W 44th St New York, NY 10036',
                          merchant_logo='http://s3-media3.fl.yelpcdn.com/bphoto/LGsFzir_aKmp9uswg6MmiQ/90s.jpg'),
            MerchantModel(name='Caledonia Bar',
                          num_ratings=40,
                          overall_rating=3.4,
                          location='1609 2n,d Ave New York, NY 10028',
                          merchant_logo='http://s3-media2.fl.yelpcdn.com/bphoto/fqPnLDlIwm4Rq1kvESOgEg/90s.jpg'),
            MerchantModel(name='Cock & Bull',
                          num_ratings=80,
                          overall_rating=4.3,
                          location='23 W 45th St New York, NY 10036',
                          merchant_logo='http://s3-media4.fl.yelpcdn.com/bphoto/L48DkrjlPJnl1Y_5YWu8pQ/90s.jpg')
        ]

        response = []
        products = ProductModel.query().fetch()

        for merchant in merchants:
            merchant.put()
            total_beers = random.uniform(10, 20)
            random.shuffle(products)
            for product in products[:int(total_beers)]:
                if not product.merchant:
                    product.merchant = []
                product.merchant.append(merchant)
            response.append(merchant.to_dict(include=MerchantModel.get_public_properties()))

        for product in products:
            product.put()

        return response




