from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
import app.config as config
from app.commands import create_tables, add_user, create_test_tables
import os
import logging
from logging.handlers import RotatingFileHandler

from app.extentions import db, login_manager

app = Flask(__name__)
app.config.from_object(config)
mail = Mail()

db.init_app(app)
mail.init_app(app)

login = LoginManager(app)
login.login_view = 'login'

app.cli.add_command(create_tables)
app.cli.add_command(create_test_tables)
app.cli.add_command(add_user)

os.makedirs('logs', exist_ok=True)
file_handler = RotatingFileHandler('logs/FrontEndCorrect.log',
                                   maxBytes=10240, backupCount=10)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s '
    '[in %(pathname)s:%(lineno)d]'))
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)

app.logger.setLevel(logging.INFO)
app.logger.info('FrontEndCorrect startup')

from app import routes, models
