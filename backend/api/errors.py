import json


class ApiException(Exception):
    status_code = 500
    message = 'Something went horribly wrong and we can not even describe it!'
    payload = {}

    def __init__(self, message=None, status_code=None, payload=None):
        Exception.__init__(self)
        if message is not None:
            self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = {
            'errors': self.payload or {},
            'description': self.message
        }
        return rv

    def __str__(self):
        return json.dumps(self.to_dict())


class InvalidUsage(ApiException):
    status_code = 400
    message = 'Sorry, this task failed. Try again and if this persists contact %s.' % 'saj.arora24@gmail.com'


class Unauthorized(ApiException):
    status_code = 401
    message = 'Please log in or sign up to continue.'


class Forbidden(ApiException):
    status_code = 403
    message = 'Forbidden, you do not have access to this resource.'


class NotFound(ApiException):
    status_code = 404
    message = 'Resource not found.'


Error = {  # regular errors
    400: InvalidUsage,
    401: Unauthorized,
    403: Forbidden,
    404: NotFound,
    500: ApiException
}


def create(code, payload=None, message=None):
    error = Error.get(code, Error.get(500))
    raise error(message=message, payload=payload)
