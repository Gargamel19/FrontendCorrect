from flask import Flask
from flask_login import LoginManager
import app.config as config
from app.commands import create_tables, add_user

from app.extentions import db, login_manager

app = Flask(__name__)
app.config.from_object(config)

db.init_app(app)

login = LoginManager(app)
login.login_view = 'login'

app.cli.add_command(create_tables)
app.cli.add_command(add_user)

from app import routes, models
