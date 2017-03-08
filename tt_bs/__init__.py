import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object('config')
#app.config.from_object('mysecret')

db = SQLAlchemy(app)
basedir = os.path.abspath(os.path.dirname(__file__))


if not app.debug:
    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler(os.path.join(basedir, '..', 'warning.log'))
    file_handler.setLevel(logging.WARNING)
    app.logger.addHandler(file_handler)


from tt_bs import models, routes