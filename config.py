"""Flask configuration."""
from os import environ, path
from dotenv import load_dotenv
import redis

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))



class Config:
    """Base config."""
    FLASK_APP = 'wsgi.py'
    SECRET_KEY = environ.get('SECRET_KEY')

    # Recaptcha
    RECAPTCHA_PUBLIC_KEY = environ.get('RECAPTCHA_PUBLIC_KEY')
    RECAPTCHA_PRIVATE_KEY = environ.get('RECAPTCHA_PRIVATE_KEY')

    # SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False


    # Flask-Mail
    MAIL_SERVER = environ.get('MAIL_SERVER')
    MAIL_PORT = environ.get('MAIL_PORT')
    MAIL_USERNAME = environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = environ.get('MAIL_PASSWORD')
    MAIL_USE_SSL = environ.get('MAIL_USE_SSL')

    # Stream
    STREAM_API_KEY = environ.get('STREAM_API_KEY')
    STREAM_SECRET = environ.get('STREAM_SECRET')


class ProdConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = environ.get('PROD_DATABASE_URI')


class DevConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = environ.get('DEV_DATABASE_URI_1')

    # Flask-Assets
    ASSETS_DEBUG = True
    COMPRESSOR_DEBUG = True
