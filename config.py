# config.py

import os


class Config(object):
    DEBUG = False
    CSRF_ENABLED = True
    SECRET_KEY = 'my_secret_key'
    SQLALCHEMY_DATABASE_URI ='postgresql://tthdmvvrjyuwes:491a8794394522641b936296e1525ef4d840ef88fada39f5e8428a7d2453d09a@ec2-3-231-69-204.compute-1.amazonaws.com:5432/dakm8ep7k876s3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
