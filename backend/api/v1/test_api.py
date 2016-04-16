"""
Project: backend
Author: Saj Arora
Description: 
"""
from api import make_empty_ok_response, make_json_ok_response
from api.models import TestModel
from main import API
from flask_restful import Resource

from flask_restful import reqparse


@API.resource('/api/v1/test')
class TestResource(Resource):
    def get(self):
        print 'here'
        return make_json_ok_response(dict(Test="v1"))

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True)
        parser.add_argument('place')
        args = parser.parse_args()
        test = TestModel(**args)
        test.put()
        return test.to_dict(include=TestModel.PUBLIC_PROPERTIES)