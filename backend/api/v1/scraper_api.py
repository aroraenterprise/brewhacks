"""
Project: backend
Author: Saj Arora
Description: 
"""
import json
import urllib

from google.appengine.api import urlfetch, memcache
from google.appengine.ext import deferred

import scraper
from api import make_empty_ok_response, errors, make_json_ok_response
from main import API
from flask_restful import Resource

from flask_restful import reqparse

KEY_SCRAPER_DELIVERY = 'scraper.delivery'

@API.resource('/api/v1/scraper/delivery')
class ScraperResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('address', required=True)
        args = parser.parse_args()

        # get delivery data
        # client = memcache.Client()
        #
        # data = client.get(KEY_SCRAPER_DELIVERY + args.get('address'))

        # https://www.delivery.com/api/data/search?
        # section=beer&address=119%20W%2024th%20St%2C%2010011&
        # order_type=delivery&
        # order_time=ASAP&
        # limit_if_segmented=20&
        # search_type=Alcohol&
        # iso=true&client_id=MDlkMzY3Nzg3MjU1ZjRkNmY4OWZjNDA0NjBjMTI0MWZl

        query_params = urllib.urlencode(dict(
            section='beer',
            limit_if_segmented=20,
            subsection='lager',
            address=args.get('address'),
            order_time='ASAP',
            search_type='alcohol',
            client_id='brewhacks2016'
        ))
        # if not data:
        url = "https://www.delivery.com/api/data/search?section=beer&subsection=lager&address=119%20W%2024th%20St%2C%2010011&order_type=delivery&order_time=ASAP&limit_if_segmented=20&search_type=Alcohol&iso=true&client_id=MDlkMzY3Nzg3MjU1ZjRkNmY4OWZjNDA0NjBjMTI0MWZl"
        result = urlfetch.fetch(url)
        if result.status_code == 200:
            data = json.loads(result.content)
                # if data:
                #     client.set(KEY_SCRAPER_DELIVERY + args.get('address'), data)

        # if not data:
        #     errors.create(500, message="No data found")

        # parse this data
        # deferred.defer(scraper.parse_delivery, data.get('data'))
        data = scraper.parse_delivery(data.get('data'))
        return data
