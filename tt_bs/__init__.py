import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address



app = Flask(__name__)
app.config.from_object('config')
CORS(app)
#app.config.from_object('mysecret')

limiter = Limiter(
    app,
    key_func=get_remote_address,
    global_limits=["2000 per day", "200 per hour"]
)

db = SQLAlchemy(app)
basedir = os.path.abspath(os.path.dirname(__file__))


if not app.debug:
    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler(os.path.join(basedir, '..', 'warning.log'))
    file_handler.setLevel(logging.WARNING)
    app.logger.addHandler(file_handler)


from tt_bs import models, routes