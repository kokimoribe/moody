"""Custom exceptions are defined here."""

class BaseError(Exception):

    status = 500

    def __init__(self, message):
        self.message = message

    def to_dict(self):
        return {
            'status': self.status,
            'message': self.message
        }


class UnauthorizedError(BaseError):
    status = 401


class NotFoundError(BaseError):
    status = 404
