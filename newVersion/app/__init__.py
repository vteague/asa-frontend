import datetime
import os

import sys
from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from config import config

db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)

    # register all script
    from .script import script
    app.register_blueprint(script, url_prefix='/')

    app.secret_key = os.urandom(16)
    app.permanent_session_lifetime = datetime.timedelta(
        hours=app.config.get('SESSION_EXPIRATION', 12))  # If not set, the default is 12 hours.
    return app
