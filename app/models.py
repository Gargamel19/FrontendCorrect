from datetime import datetime, timedelta

from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import UserMixin

from app import login
from app import db
import random
import string


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    one_time_link_hash = db.Column(db.String(128))
    one_time_link_date = db.Column(db.DateTime(), index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def make_one_time_link(self):
        chars = string.ascii_uppercase + string.digits
        self.one_time_link_hash = ''.join(random.choice(chars) for _i in range(30))
        self.one_time_link_date = datetime.now() + timedelta(minutes=10)
        db.session.commit()
        return self.one_time_link_hash
