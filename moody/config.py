"""Configuration and secret values are defined here"""
import os

DEBUG = os.environ.get('DEBUG', False)
DATABASE_URL = os.environ['DATABASE_URL']
GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY']
JWT_SECRET = os.environ['JWT_SECRET']
JWT_ISSUER = os.environ.get('JWT_ISSUER', 'moody')
JWT_DURATION = os.environ.get('JWT_DURATION', 86400)
