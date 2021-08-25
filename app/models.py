from datetime import datetime, timedelta

from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import UserMixin

from app import login
from app.extentions import db
import random
import string


@login.user_loader
def load_user(aid):
    return User.query.get(int(aid))


class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    one_time_link_hash = db.Column(db.String(128))
    one_time_link_date = db.Column(db.DateTime(), index=True, default=datetime.utcnow)
    super_user = db.Column(db.Boolean())

    def __init__(self, username, email, super_user):
        self.username = username
        self.email = email
        self.super_user = super_user

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def set_mail(self, mail):
        self.email = mail

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def make_one_time_link(self):
        chars = string.ascii_uppercase + string.digits
        self.one_time_link_hash = ''.join(random.choice(chars) for _i in range(30))
        self.one_time_link_date = datetime.now() + timedelta(minutes=10)
        db.session.commit()
        return self.one_time_link_hash

    def save_user(self):
        print(db)
        db.session.add(self)
        db.session.commit()
