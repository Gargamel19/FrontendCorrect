import os
import unittest

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import app.config_test as config
from app.models import User

import tempfile
from app import app

class UserTests(unittest.TestCase):

    ############################
    #    setup and teardown    #
    ############################
    db = SQLAlchemy()
    def create_app(self):

        app.config.from_object(config)
        self.db.init_app(app)

        # create routes, etc.

        return app

    # executed prior to each test
    def setUp(self):
        app = self.create_app()
        self.app = app.test_client()
        return app

    # executed after each test
    def tearDown(self):
        pass

    ###############
    #    tests    #
    ###############

    def test_login_page(self):
        response = self.app.get("/login")
        self.assertEqual(response.status_code, 200)
        print("test_login_page OK")


if __name__ == "__main__":
    unittest.main()
