from flask import Flask
from flask_login import LoginManager
import app.config as config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)
db.create_all()
migrate = Migrate(app, db)

login = LoginManager(app)
login.login_view = 'login'

from app import routes, models
