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

    # Flask-Session
    REDIS_URI = environ.get("REDIS_URI")
    SESSION_TYPE = "redis"
    SESSION_REDIS = redis.from_url(REDIS_URI)


class ProdConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = environ.get('PROD_DATABASE_URI')


class DevConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = environ.get('DEV_DATABASE_URI')

    # Flask-Assets
    ASSETS_DEBUG = True
    COMPRESSOR_DEBUG = True


class TestingConfig(Config):
    FLASK_ENV = 'testing'
    SQLALCHEMY_DATABASE_URI = environ.get('TEST_DATABASE_URI')
    DEBUG = True
    TESTING = True
    # Flask-Assets

    ASSETS_DEBUG = True
    COMPRESSOR_DEBUG = True
