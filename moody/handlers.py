"""
Functions that handle Flask app/request/response lifecycle events are defined here.
"""

from flask import jsonify, current_app as app

from moody.db import session


def handle_custom_error(exception):
    response = {
        'message': exception.message,
        'status': exception.status
    }

    return jsonify(response), exception.status


def handle_marshmallow_error(exception):
    status = 400

    response = {
        'message': str(exception),
        'status': status
    }

    return jsonify(response), status


def handle_general_error(exception):
    response = {
        'message': 'A server side error has occurred. Please try again later.',
        'status': 500
    }
    app.logger.exception(exception)

    return jsonify(response), 500


def handle_app_teardown(exception=None):
    """Remove db session on teardown"""
    session.remove()
