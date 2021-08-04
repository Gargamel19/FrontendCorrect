import click
from flask.cli import with_appcontext
from app.extentions import db


@click.command(name='create_tables')
@with_appcontext
def create_tables():
    print("create tables")
    from app import app
    print(app.config["SQLALCHEMY_DATABASE_URI"])
    db.create_all()


@click.command(name='create_test_tables')
@with_appcontext
def create_test_tables():
    print("create test tables")
    from app import app
    import app.config_test as config_test
    app.config["SQLALCHEMY_DATABASE_URI"] = config_test.SQLALCHEMY_DATABASE_URI
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
