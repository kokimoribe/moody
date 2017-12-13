"""
Create flask app
"""
from logging.handlers import RotatingFileHandler
import logging

from flask import Flask
from flask_cors import CORS
from marshmallow.exceptions import ValidationError

from moody.routes import main
from moody.db import session
from moody.exceptions import UnauthorizedError
from moody.handlers import (
    handle_custom_error,
    handle_general_error,
    handle_app_teardown,
    handle_marshmallow_error
)


app = Flask(__name__)

# Register routes from main blueprint
app.register_blueprint(main)

# Add file logging
file_handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=1)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s '
    '[in %(pathname)s:%(lineno)d]'
))
file_handler.setLevel(logging.WARNING)
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)

# Add handlers
app.register_error_handler(UnauthorizedError, handle_custom_error)
app.register_error_handler(ValidationError, handle_marshmallow_error)
app.register_error_handler(Exception, handle_general_error)
app.teardown_appcontext_funcs.append(handle_app_teardown)

# Add CORS
CORS(app)
