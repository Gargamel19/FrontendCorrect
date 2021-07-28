import os
from dotenv import load_dotenv
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

BASEDIR = os.path.abspath(os.path.dirname(__file__))
SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(BASEDIR, 'tests_app.db')
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
if os.environ.get('BACKEND_PORT'):
    BACKEND_PORT = int(os.environ.get('BACKEND_PORT'))
else:
    BACKEND_PORT = 5001

START_PORT = 0

# MAIL
SMTP_SERVER = os.environ.get('MAIL_SERVER')
TLS_PORT = int(os.environ.get('MAIL_PORT') or 25)
MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_SECRET = os.environ.get('MAIL_PASSWORD')
MAIL_ADMINS = os.environ.get('MAIL_ADMINS').split(';') if os.environ.get('MAIL_ADMINS') else ['no-reply@example.com']
