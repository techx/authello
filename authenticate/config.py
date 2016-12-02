import os

class Config(object):
  DEBUG = False
  TESTING = False
  SQLALCHEMY_DATABASE_URI = 'sqlite://:memory:'
  SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
  SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', None)
  SECRET_KEY = os.getenv('SECRET_KEY', None)

class DevConfig(Config):
  DEBUG = True
  SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.path.dirname(__file__), '..', 'dev.db')
  SQLALCHEMY_TRACK_MODIFICATIONS = True
  SECRET_KEY = 'this-is-a-super-secret-key'
