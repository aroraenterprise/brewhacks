"""
Project: backend
Author: Saj Arora
Description: 
"""
import json

from google.appengine.api import urlfetch, memcache

import scraper
from api import make_empty_ok_response, errors, make_json_ok_response
from main import API
from flask_restful import Resource

KEY_SCRAPER_DELIVERY = 'scraper.delivery.new'

@API.resource('/api/v1/scraper/delivery')
class ScraperResource(Resource):
    def post(self):
        # get delivery data
        client = memcache.Client()

        data = client.get(KEY_SCRAPER_DELIVERY)

        if not data:
            url = "https://www.delivery.com/api/data/search?section=beer&" \
                  "address=119%20W%2024th%20St%2C%2010011&order_type=delivery" \
                  "&order_time=ASAP&limit_if_segmented=20&search_type=" \
                  "Alcohol&iso=true&client_id=brewhacks2016"
            result = urlfetch.fetch(url)
            if result.status_code == 200:
                data = json.loads(result.content)
                if data:
                    client.set(KEY_SCRAPER_DELIVERY, data)

        if not data:
            errors.create(500, message="No data found")

        # parse this data
        return scraper.parse_delivery(data.get('data'))
