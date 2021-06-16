import click
from flask.cli import with_appcontext

import app.config
from app.extentions import db


@click.command(name='create_tables')
@with_appcontext
def create_tables():
    print("create tables")
    print(app.config.SQLALCHEMY_DATABASE_URI)
    db.create_all()


@click.command(name='add_user')
@with_appcontext
@click.argument("name")
@click.argument("email")
@click.argument("pw")
@click.argument("su")
def add_user(name, email, pw, su):
    print("add_user")
    print(name, email, pw, su)
    from app import routes
    routes.add_user(name, email, pw, su == "True")
