"""Functions for handling authorization are defined here"""

from functools import wraps

from flask import request, g
import arrow
import jwt

from moody.config import JWT_SECRET, JWT_DURATION, JWT_ISSUER
from moody.exceptions import UnauthorizedError


def require_token(fn):
    """Function used to decorate routes that require authorization."""
    @wraps(fn)
    def wrapped(*args, **kwargs):
        token = get_token_from_request()
        payload = decode_token(token)
        g.validated_token = payload

        return fn(*args, **kwargs)
    return wrapped


def create_token(user, duration=JWT_DURATION):
    """Encode and sign a authorization token for user"""

    issued_at = arrow.utcnow()
    expires_at = issued_at.shift(seconds=duration)

    payload = {
        'email': user.email,
        'iss': JWT_ISSUER,
        'iat': issued_at.datetime,
        'exp': expires_at.datetime,
    }

    token = jwt.encode(payload, JWT_SECRET, algorithm='HS256').decode()

    return token


def get_token_from_request():
    auth_header = request.headers.get('Authorization', None)

    if not auth_header:
        raise UnauthorizedError("Missing 'Authorization' header.")

    if not auth_header.startswith("Bearer "):
        raise UnauthorizedError("Must set 'Authorization' header to 'Bearer {token}'.")

    token = auth_header.split("Bearer ")[1]

    return token


def decode_token(token):
    try:
        payload = jwt.decode(token.encode('utf-8'), JWT_SECRET)
    except jwt.exceptions.InvalidTokenError as error:
        raise UnauthorizedError(str(error))

    return payload
