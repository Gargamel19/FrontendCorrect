import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))
SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(BASEDIR, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(BASEDIR, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = True

# IP

MY_IP = "https://correctfrontend.herokuapp.com/"

# BACKEND
BACKEND_IP = "https://be-correct.herokuapp.com/"
BACKEND_PORT = 5001

START_PORT = 0

# MAIL
MAIL_USERNAME = "notreply.supersicher@gmail.com"
MAIL_SECRET = "supersicherespasswort"
SMTP_SERVER = "smtp.gmail.com"
TLS_PORT = 587