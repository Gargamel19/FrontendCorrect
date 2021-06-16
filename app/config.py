import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))
SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
SQLALCHEMY_DATABASE_URI = "postgres://uveifpynzjoosq:1d02813dfd2dfcdda3ef7c154f8047ad6a7a601aa1ae03e06954540495d4be24@ec2-54-228-139-34.eu-west-1.compute.amazonaws.com:5432/d4mujlupdais5d"
#SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(BASEDIR, 'app.db')
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