import os
from datetime import timedelta


class Config:
    ENV = 'production'
    SECRET_KEY = 'enter a secret key'
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:root@localhost:5432/test-db"
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME' , '')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD' , '')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', 'authelectric@gmail.com')
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', True)
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL', False)
    REMEMBER_COOKIE_DURATION = timedelta(hours=24)
    ENCRYPT_KEY = ''
    ENCRYPT_IV = ''
    JWT_SECRET_KEY = "please-remember-to-change-me"
    # REMEMBER_COOKIE_PATH = 
    # REMEMBER_COOKIE_SECURE =
    # REMEMBER_COOKIE_HTTPONLY =
    RATELIMIT_DEFAULT = '50/hour;100/day;2000/year'
    RATELIMIT_STORAGE_URL = 'redis://localhost:6379'
    TWILIO_ACCOUNT_SID = 'ACb083c410c171a6f23863e6b65c6ea1bc'
    TWILIO_AUTH_TOKEN = 'f4cb26461776c2502396af3e56a38ec6'

'''
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
'''

class DevelopmentConfig(Config):
    ENV = 'development'
    DEBUG = False
    SECRET_KEY = 'enter a key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI', Config.SQLALCHEMY_DATABASE_URI)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    RATELIMIT_DEFAULT = '10/hour;100/day;2000 per year'

    

'''
class TestingConfig(Config):
    DEBUG = False
    ENV = 'testing'
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SECRET_KEY = 'e0ad86e4a68d6aeef26cb571ea7a6524c3aebc825a452b375007dff823645e4f'
    WTF_CSRF_ENABLED = False
    MAIL_SUPPRESS_SEND = True
'''
