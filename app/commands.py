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
