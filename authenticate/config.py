import os

class Config(object):
  DEBUG = False
  TESTING = False
  SQLALCHEMY_DATABASE_URI = 'sqlite://:memory:'

class ProductionConfig(Config):
  SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', None)

class DevConfig(Config):
  DEBUG = True
  SQLALCHEMY_DATABASE_URI = os.path.join(os.path.dirname(__file__), '..', 'auth.db')
