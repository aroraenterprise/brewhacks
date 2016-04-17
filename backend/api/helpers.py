# coding: utf-8
"""
Set of helper function used throughout the REST API
"""
import json
import logging

import flask
import flask_restful as restful
from werkzeug import exceptions

from api import errors


class Api(restful.Api): # pylint: disable=too-few-public-methods
    """By extending restful.Api class we can make custom implementation of some of its methods"""
    def handle_error(self, err):
        """Specifies error handler for REST API.
        It is called when exception is raised during request processing

        Args:
            err (Exception): the raised Exception object

        """
        return handle_error(err)


def handle_error(err):
    """This error handler logs exception and then makes response with most
    appropriate error message and error code

    Args:
        err (Exception): the raised Exception object

    """
    logging.exception(err)
    message = ''
    if hasattr(err, 'data') and err.data['message']:
        message = err.data['message']
    elif hasattr(err, 'message') and err.message:
        message = err.message
    elif hasattr(err, 'description'):
        message = err.description
    try:
        err.code
    except AttributeError:
        err.code = 500

    if isinstance(err, errors.ApiException):
        response = flask.jsonify(err.to_dict())
        response.status_code = err.status_code
        return response, err.status_code
    else:
        return flask.jsonify({
            'message': message
        }), err.code


def make_not_found_exception():
    """Raises 404 Not Found exception

    Raises:
        HTTPException: with 404 code
    """
    raise errors.create(404)


def make_bad_request_exception(message):
    """Raises 400 Bad request exception

    Raises:
        HTTPException: with 400 code
    """
    raise errors.create(400)


def make_empty_ok_response():
    """Returns OK response with empty body"""
    return '', 204


def make_json_ok_response(data):
    """Returns OK response with json body"""
    return data


def make_search_list_response(reponse_list, offset=None, more=False, total_count=None):
    """Creates reponse with list of search items and also meta data useful for pagination

    Args:
        reponse_list (list): list of items to be in response
        cursor (Cursor, optional): ndb query cursor
        more (bool, optional): whether there's more items in terms of pagination
        total_count (int, optional): Total number of items

    Returns:
        dict: response to be serialized and sent to client
    """
    return {
        'list': reponse_list,
        'meta': {
            'offset': offset,
            'more': more,
            'totalCount': total_count
        }
    }


def make_list_response(response_list, cursor=None, more=False, total_count=None):
    """Creates reponse with list of items and also meta data useful for pagination

    Args:
        reponse_list (list): list of items to be in response
        cursor (Cursor, optional): ndb query cursor
        more (bool, optional): whether there's more items in terms of pagination
        total_count (int, optional): Total number of items

    Returns:
        dict: response to be serialized and sent to client
    """
    return {
        'list': response_list,
        'meta': {
            'nextCursor': cursor.urlsafe() if cursor else '',
            'more': more,
            'totalCount': total_count
        }
    }




