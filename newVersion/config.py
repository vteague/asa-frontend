# -*- coding=utf-8 -*-
import logging
import os
from logging.handlers import RotatingFileHandler


class Config:
    SECRET_KEY = ''  # input the secret key
    # SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    @staticmethod
    def init_app(app):
        handler = RotatingFileHandler('back.log', maxBytes=10000, backupCount=1)
        handler.setLevel(logging.WARNING)
        app.logger.addHandler(handler)


# the config for development
class DevelopmentConfig(Config):
    DB_USER = 'root'
    DB_PASSWORD = 'root'
    DB_HOST = 'localhost'
    DB_DB = 'ASAFrontend'

    PORT = 3306
    SQLALCHEMY_DATABASE_URI = 'mysql://' + DB_USER + ':' + DB_PASSWORD + '@' + DB_HOST + '/' + DB_DB
    DEBUG = True

    SESSION_EXPIRATION = 12  # Session Expiration，hours
    PROJECT_DIR=os.path.dirname(os.path.abspath(__file__)) #project_dir

# define the config
config = {
    'default': DevelopmentConfig
}
