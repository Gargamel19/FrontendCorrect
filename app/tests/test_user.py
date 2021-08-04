
import unittest

import app.config_test as config_test

from app.models import User
from app import app, db


class UserTests(unittest.TestCase):

    loged_in_normal_routes = \
        [
            ["/", 200, 302],
            ["/sammlung/mondsee", 200, 302],
            ["/sammlung/mondsee/text/mondsee.rath0001.lat001.xml", 200, 302],
            ["/sammlung/mondsee/text/mondsee.rath0001.lat001.xml/backups", 200, 302],
            ["/change_mail", 200, 302],

            ["/logout", 302, 302],
        ]

    loged_in_superuser_routes = \
        [
            ["/register", 200, 302],
        ]

    not_loged_in_routes = \
        [
            ["/login", 200],
            ["/change_pw", 200],
        ]

    def create_app(self):
        app.config.from_object(config_test)
        db.init_app(app)

        return app

    def addUser(self):
        with app.app_context():
            user = User("testuser", "trendelenburger19.04@googlemail.com", False)
            user.set_password("Pa55wort")
            db.session.add(user)
            user = User("superuser", "trendelenburger19.041@googlemail.com", True)
            user.set_password("Pa55wort")
            db.session.add(user)
            db.session.commit()

    # executed prior to each test
    def setUp(self):

        self.app = self.create_app()
        self.client = self.app.test_client()
        self._ctx = self.app.test_request_context()
        self._ctx.push()

        db.init_app(app)
        db.create_all()
        self.addUser()

    def tearDown(self):

        db.session.remove()
        db.drop_all()

    def expectGetStatus(self, c, url, status):
        response = c.get(url)
        if response.status_code == status:
            print("\t" + url + " ✔️")
        else:
            print("\t" + url + " ❌")
        self.assertEqual(response.status_code, status)

    def test_not_logged_in(self):
        with self.client as c:
            print()
            print("not_logged_in_allowed_pages:")
            for route in self.not_loged_in_routes:
                self.expectGetStatus(c, route[0], route[1])

            print()
            print("not_logged_in_restricted_pages:")

            for route in self.loged_in_superuser_routes:
                self.expectGetStatus(c, route[0], route[2])
            for route in self.loged_in_normal_routes:
                self.expectGetStatus(c, route[0], route[2])

    def test_logged_in_normal(self):
        with self.client as c:
            print()
            print("logged_in_normal_allowed_pages:")

            c.post("/login", data=dict(username='testuser', password="Pa55wort",
                   follow_redirects=True))
            for route in self.loged_in_normal_routes:
                self.expectGetStatus(c, route[0], route[1])
            print()
            print("logged_in_normal_restricted_pages:")

            for route in self.loged_in_superuser_routes:
                self.expectGetStatus(c, route[0], route[2])

    def test_logged_in_superuser_allowed_pages(self):

        with self.client as c:
            print()
            print("logged_in_superuser_allowed_pages:")

            c.post("/login", data=dict(username='superuser', password="Pa55wort",
                   follow_redirects=True))
            for route in self.loged_in_superuser_routes:
                self.expectGetStatus(c, route[0], route[1])




if __name__ == "__main__":
    unittest.main()
