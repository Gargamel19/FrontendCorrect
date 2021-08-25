
import unittest
from unittest.mock import Mock, patch

import app.config_test as config_test


from app.models import User
from app import app, db

from flask import template_rendered

class UserTests(unittest.TestCase):

    loged_in_normal_routes = \
        [
            ["/", "index.html", '["mondsee"]', "login.html"],
            ["/sammlung/mondsee", "index_ueberlieferung.html", '["text1", "text2", "text3"]', "login.html"],
            ["/sammlung/mondsee/text/mondsee.rath0001.lat001.xml", "index_ueberlieferung_text.html", '[{"function": "test", "words": [["Ego", {"function": "test", "style": "kursiv"}], [" ", {}]]}]', "login.html"],
            ["/sammlung/mondsee/text/mondsee.rath0001.lat001.xml/backups", "index_backups.html", '["mondsee.rath0001.lat001-2021-08-04-16-23-55.062899_r_.xml", "mondsee.rath0001.lat001-2021-08-04-17-23-55.062899_r_.xml", "mondsee.rath0001.lat001-2021-08-04-18-23-55.062899_r_.xml"]', "login.html"],
            ["/sammlung/mondsee/text/mondsee.rath0001.lat001.xml/backup/mondsee.rath0001.lat001-2021-08-04-16-23-55.062899_r_.xml", "index_backup_text.html",
             '[]',
             "login.html"],

            ["/change_mail", "change_mail.html", "", "login.html"],

            ["/logout", "login.html", True, "login.html"],
        ]

    loged_in_superuser_routes = \
        [
            ["/register", "register.html", "", "login.html"],
        ]

    not_loged_in_routes = \
        [
            ["/login", "login.html"],
            ["/change_pw", "request_otl.html"],
        ]

    def _add_template(self, app, template, context):
        if len(self.templates) > 0:
            self.templates = []
        self.templates.append((template, context))

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

        self.templates = []
        template_rendered.connect(self._add_template)

    def tearDown(self):

        template_rendered.disconnect(self._add_template)
        db.session.remove()
        db.drop_all()

    def expectGetStatus(self, c, url, template):
        c.get(url, follow_redirects=True)
        if template in [x[0].name for x in self.templates]:
            print("\t" + url + " ✔️")
        else:
            print("\t" + url + " ❌")
        self.assertIn(template, [x[0].name for x in self.templates])

    def test_not_logged_in(self):
        with self.client as c:
            print()
            print("not_logged_in_allowed_pages:")
            for route in self.not_loged_in_routes:
                self.expectGetStatus(c, route[0], route[1])

            print()
            print("not_logged_in_restricted_pages:")

            for route in self.loged_in_superuser_routes:
                self.expectGetStatus(c, route[0], route[3])
            for route in self.loged_in_normal_routes:
                self.expectGetStatus(c, route[0], route[3])

    def test_logged_in_normal(self):
        with self.client as c:
            print()
            print("logged_in_normal_allowed_pages:")

            c.post("/login", data=dict(username='testuser', password="Pa55wort",
                   follow_redirects=True))

            mock_get_patcher = patch('app.routes.requests.get')
            mock_get = mock_get_patcher.start()

            for route in self.loged_in_normal_routes:

                mock_get.return_value = Mock(text=route[2])

                self.expectGetStatus(c, route[0], route[1])

            print()
            print("logged_in_normal_restricted_pages:")

            mock_get_patcher.stop()

            for route in self.loged_in_superuser_routes:
                self.expectGetStatus(c, route[0], route[3])

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
