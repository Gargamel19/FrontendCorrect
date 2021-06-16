import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))
SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(BASEDIR, 'app.db')
if SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)
SQLALCHEMY_MIGRATE_REPO = os.path.join(BASEDIR, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = True

# IP

MY_IP = os.environ.get('MY_IP') or "http://127.0.0.1:5000/"

# BACKEND
#BACKEND_IP = "https://be-correct.herokuapp.com/"
BACKEND_IP = os.environ.get('BACKEND_IP') or "http://127.0.0.1"
#BACKEND_PORT = 80
BACKEND_PORT = int(os.environ.get('BACKEND_PORT')) or 5001

START_PORT = 0

# MAIL
MAIL_USERNAME = "notreply.supersicher@gmail.com"
MAIL_SECRET = "supersicherespasswort"
SMTP_SERVER = "smtp.gmail.com"
TLS_PORT = 587