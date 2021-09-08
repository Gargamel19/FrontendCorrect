
import unittest
from unittest.mock import Mock, patch

import app.config_test as config_test

from app.models import User
from app import app, db, routes

from flask import template_rendered


class UserTests(unittest.TestCase):

    not_logged_in = [
        {"function": "GET", "url": "/login", "template": "login.html"},
        {"function": "GET", "url": "/logout", "template": "login.html"},
        {"function": "GET", "url": "/register", "template": "login.html"},
        {"function": "GET", "url": "/change_pw", "template": "request_otl.html"},
        {"function": "GET", "url": "/change_pw?otl=OTL", "template": "change_pw.html", "otl": "testuser"},
        {"function": "GET", "url": "/change_mail", "template": "login.html"},
        {"function": "GET", "url": "/change_mail?otl=OTL&email=hallo@gmail.com", "template": "login.html", "otl": "testuser"},
        {"function": "GET", "url": "/", "template": "login.html"},
        {"function": "GET", "url": "/sammlung/mondsee", "template": "login.html"},
        {"function": "GET", "url": "/sammlung/mondsee/text/mondsee.rath0001.lat001.xml", "template": "login.html"},
        {"function": "GET", "url": "/sammlung/mondsee/text/mondsee.rath0001.lat001.xml/backups", "template": "login.html"},
        {
            "function": "GET",
            "url": "/sammlung/mondsee/text/mondsee.rath0001.lat001.xml/backup/mondsee.rath0001.lat001-2021-08-04-16-23-55.062899_r_.xml",
            "template": "login.html"
        },
        {
            "function": "POST",
            "url": "/login",
            "form": dict(username='testuser', password="Pa55wort"),
            "template": "index.html",
            "request_mock_return_get": '["mondsee"]',
            "logout": True
        },
        {
            "function": "POST",
            "url": "/register",
            "form": dict(username='testuser1', password="Pa55wort"),
            "template": "login.html"},
        {
            "function": "POST",
            "url": "/change_pw?otl=OTL",
            "form": dict(password='IchBin1Giraffe', password2="IchBin1Giraffe"),
            "template": "login.html",
            "otl": "testuser"},
        {
            "function": "POST",
            "url": "/change_pw",
            "form": dict(password='IchBin1Giraffe', password2="IchBin1Giraffe"),
            "template": "login.html",
        },
        {
            "function": "POST",
            "url": "/change_mail",
            "form": dict(),
            "template": "login.html",
        },
        {
            "function": "POST",
            "url": "/sammlung/mondsee/text/mondsee.rath0001.lat001.xml",
            "form": dict(),
            "template": "login.html",
        },
        {
            "function": "POST",
            "url": "/sammlung/mondsee/text/mondsee.rath0001.lat001.xml/backup/mondsee.rath0001.lat001-2021-08-04-16-23-55.062899_r_.xml",
            "form": dict(),
            "template": "login.html",
        },
    ]

    normal_user_logged_in = [
        {
            "function": "GET",
            "url": "/login",
            "template": "index.html",
            "request_mock_return_get": '["mondsee"]',
        },
        {
            "function": "GET",
            "url": "/logout",
            "template": "login.html",
        },
        {
            "function": "GET",
            "url": "/register",
            "template": "index.html",
            "request_mock_return_get": '["mondsee"]',
        },
        {
            "function": "GET",
            "url": "/change_pw",
            "template": "change_pw.html"
        },
        {
            "function": "GET",
            "url": "/change_pw?otl=OTL",
            "template": "change_pw.html",
            "otl": "testuser"
        },
        {
            "function": "GET",
            "url": "/change_mail",
            "template": "change_mail.html"
        },
        {
            "function": "GET",
            "url": "/change_mail?otl=OTL&email=hallo@gmail.com",
            "template": "index.html",
            "otl": "testuser",
            "request_mock_return_get": '["mondsee"]'
        },
        {
            "function": "GET",
            "url": "/",
            "template": "index.html",
            "request_mock_return_get": '["mondsee"]',
        },
        {
            "function": "GET",
            "url": "/sammlung/mondsee",
            "template": "index_ueberlieferung.html",
            "request_mock_return_get": '["text1", "text2", "text3"]',
        },
        {
            "function": "GET",
            "url": "/sammlung/mondsee/text/mondsee.rath0001.lat001.xml",
            "template": "index_ueberlieferung_text.html",
            "request_mock_return_get": '[{"function": "test", "words": [["Ego", {"function": "test", "style": "kursiv"}], [" ", {}]]}]',
        },
        {
            "function": "GET",
            "url": "/sammlung/mondsee/text/mondsee.rath0001.lat001.xml/backups",
            "template": "index_backups.html",
            "request_mock_return_get": '["mondsee.rath0001.lat001-2021-08-04-16-23-55.062899_r_.xml", "mondsee.rath0001.lat001-2021-08-04-17-23-55.062899_r_.xml", "mondsee.rath0001.lat001-2021-08-04-18-23-55.062899_r_.xml"]',
        },
        {
            "function": "GET",
            "url": "/sammlung/mondsee/text/mondsee.rath0001.lat001.xml/backup/mondsee.rath0001.lat001-2021-08-04-16-23-55.062899_r_.xml",
            "template": "index_backup_text.html",
            "request_mock_return_get": '[{"function": "test", "words": [["Ego", {"function": "test", "style": "kursiv"}], [" ", {}]]}]',
        },
        {
            "function": "POST",
            "url": "/login",
            "form": dict(username='testuser', password="Pa55wort"),
            "template": "index.html",
            "request_mock_return_get": '["mondsee"]',
        },
        {
            "function": "POST",
            "url": "/register",
            "form": dict(username='testuser1', password="Pa55wort"),
            "template": "index.html",
            "request_mock_return_get": '["mondsee"]',
        },
        {
            "function": "POST",
            "url": "/change_pw?otl=OTL",
            "form": dict(password='IchBin1Giraffe', password2="IchBin1Giraffe"),
            "template": "index.html",
            "otl": "testuser",
            "request_mock_return_get": '["mondsee"]',
        },
        {
            "function": "POST",
            "url": "/change_pw",
            "form": dict(password='IchBin1Giraffe', password2="IchBin1Giraffe"),
            "template": "index.html",
            "request_mock_return_get": '["mondsee"]',
        },
        {
            "function": "POST",
            "url": "/change_mail",
            "form": dict(mail1="trendelenburger19.04@googlemail.com", mail2="trendelenburger19.04@googlemail.com"),
            "template": "index.html",
            "request_mock_return_get": '["mondsee"]',
        },
        {
            "function": "POST",
            "url": "/sammlung/mondsee/text/mondsee.rath0001.lat001.xml",
            "form": dict(),
            "payload": '[{"function": "test", "words": [["Ego", {"function": "test", "style": "kursiv"}], [" ", {}]]}]',
            "template": "index_ueberlieferung_text.html",
            "request_mock_return_post": '[{"function": "test", "words": [["Ego", {"function": "test", "style": "kursiv"}], [" ", {}]]}]',
            "request_mock_return_get": '[{"function": "test", "words": [["Ego", {"function": "test", "style": "kursiv"}], [" ", {}]]}]',
        },
        {
            "function": "POST",
            "url": "/sammlung/mondsee/text/mondsee.rath0001.lat001.xml/backup/mondsee.rath0001.lat001-2021-08-04-16-23-55.062899_r_.xml",
            "form": dict(),
            "template": "index_ueberlieferung_text.html",
            "request_mock_return_post": 'OK',
            "request_mock_return_get": '[{"function": "test", "words": [["Ego", {"function": "test", "style": "kursiv"}], [" ", {}]]}]',
        },
    ]

    super_user_logged_in = [
        {
            "function": "GET",
            "url": "/login",
            "template": "index.html",
            "request_mock_return_get": '["mondsee"]',
        },
        {
            "function": "GET",
            "url": "/logout",
            "template": "login.html",
        },
        {
            "function": "GET",
            "url": "/register",
            "template": "register.html",
        },
        {
            "function": "GET",
            "url": "/change_pw",
            "template": "change_pw.html"
        },
        {
            "function": "GET",
            "url": "/change_pw?otl=OTL",
            "template": "change_pw.html",
            "otl": "testuser"
        },
        {
            "function": "GET",
            "url": "/change_mail",
            "template": "change_mail.html"
        },
        {
            "function": "GET",
            "url": "/change_mail?otl=OTL&email=hallo@gmail.com",
            "template": "index.html",
            "otl": "testuser",
            "request_mock_return_get": '["mondsee"]'
        },
        {
            "function": "GET",
            "url": "/",
            "template": "index.html",
            "request_mock_return_get": '["mondsee"]',
        },
        {
            "function": "GET",
            "url": "/sammlung/mondsee",
            "template": "index_ueberlieferung.html",
            "request_mock_return_get": '["text1", "text2", "text3"]',
        },
        {
            "function": "GET",
            "url": "/sammlung/mondsee/text/mondsee.rath0001.lat001.xml",
            "template": "index_ueberlieferung_text.html",
            "request_mock_return_get": '[{"function": "test", "words": [["Ego", {"function": "test", "style": "kursiv"}], [" ", {}]]}]',
        },
        {
            "function": "GET",
            "url": "/sammlung/mondsee/text/mondsee.rath0001.lat001.xml/backups",
            "template": "index_backups.html",
            "request_mock_return_get": '["mondsee.rath0001.lat001-2021-08-04-16-23-55.062899_r_.xml", "mondsee.rath0001.lat001-2021-08-04-17-23-55.062899_r_.xml", "mondsee.rath0001.lat001-2021-08-04-18-23-55.062899_r_.xml"]',
        },
        {
            "function": "GET",
            "url": "/sammlung/mondsee/text/mondsee.rath0001.lat001.xml/backup/mondsee.rath0001.lat001-2021-08-04-16-23-55.062899_r_.xml",
            "template": "index_backup_text.html",
            "request_mock_return_get": '[{"function": "test", "words": [["Ego", {"function": "test", "style": "kursiv"}], [" ", {}]]}]',
        },
        {
            "function": "POST",
            "url": "/login",
            "form": dict(username='testuser', password="Pa55wort"),
            "template": "index.html",
            "request_mock_return_get": '["mondsee"]',
        },
        {
            "function": "POST",
            "url": "/register",
            "form": dict(username='testuser1', email="123@googlemail.com", password="Pa55wort", password2="Pa55wort"),
            "template": "index.html",
            "request_mock_return_get": '["mondsee"]',
        },
        {
            "function": "POST",
            "url": "/change_pw?otl=OTL",
            "form": dict(password='IchBin1Giraffe', password2="IchBin1Giraffe"),
            "template": "index.html",
            "otl": "testuser",
            "request_mock_return_get": '["mondsee"]',
        },
        {
            "function": "POST",
            "url": "/change_pw",
            "form": dict(password='IchBin1Giraffe', password2="IchBin1Giraffe"),
            "template": "index.html",
            "request_mock_return_get": '["mondsee"]',
        },
        {
            "function": "POST",
            "url": "/change_mail",
            "form": dict(mail1="trendelenburger19.04@googlemail.com", mail2="trendelenburger19.04@googlemail.com"),
            "template": "index.html",
            "request_mock_return_get": '["mondsee"]',
        },
        {
            "function": "POST",
            "url": "/sammlung/mondsee/text/mondsee.rath0001.lat001.xml",
            "form": dict(),
            "payload": '[{"function": "test", "words": [["Ego", {"function": "test", "style": "kursiv"}], [" ", {}]]}]',
            "template": "index_ueberlieferung_text.html",
            "request_mock_return_post": '[{"function": "test", "words": [["Ego", {"function": "test", "style": "kursiv"}], [" ", {}]]}]',
            "request_mock_return_get": '[{"function": "test", "words": [["Ego", {"function": "test", "style": "kursiv"}], [" ", {}]]}]',
        },
        {
            "function": "POST",
            "url": "/sammlung/mondsee/text/mondsee.rath0001.lat001.xml/backup/mondsee.rath0001.lat001-2021-08-04-16-23-55.062899_r_.xml",
            "form": dict(),
            "template": "index_ueberlieferung_text.html",
            "request_mock_return_post": 'OK',
            "request_mock_return_get": '[{"function": "test", "words": [["Ego", {"function": "test", "style": "kursiv"}], [" ", {}]]}]',
        },
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
            routes.add_user("testuser", "trendelenburger19.04@googlemail.com", "Pa55wort", False)
            routes.add_user("superuser", "trendelenburger19.041@googlemail.com", "Pa55wort", True)

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

    def compare_returns(self, template, url, function):
        rendered_templates = [x[0].name for x in self.templates]
        if template in rendered_templates:
            print("\t" + function + ": " + url + " -> " + template + " ✔️")
        else:
            print("\t" + function + ": " + url + " -> " + template + " ❌")
        self.assertIn(template, rendered_templates)

    def expectGetStatus(self, c, url, template, function):
        c.get(url, follow_redirects=True)
        self.compare_returns(template, url, function)

    def expectPostStatus(self, c, url, form, response_template, function):
        c.post(url, data=form, follow_redirects=True)
        self.compare_returns(response_template, url, function)

    def function_test(self, c, list, user=None, password=None):
        mock_get_patcher_get = patch('app.routes.requests.get')
        mock_request_get = mock_get_patcher_get.start()
        mock_request_get.return_value = Mock(text="")
        mock_get_patcher_post = patch('app.routes.requests.post')
        mock_request_post = mock_get_patcher_post.start()
        mock_request_post.return_value = Mock(text="")
        mock_get_patcher_smtp = patch('app.routes.smtplib.SMTP')
        mock_get_patcher_smtp.start()
        for route in list:
            if user and password:
                c.post("/login", data=dict(username=user, password=password), follow_redirects=True)
            route_url = route["url"]
            if "request_mock_return_get" in route:
                mock_request_get.return_value = Mock(text=route["request_mock_return_get"])
            if "request_mock_return_post" in route:
                mock_request_post.return_value = Mock(text=route["request_mock_return_post"])
            if "otl" in route:
                user = User.query.filter_by(username=route["otl"]).first()
                route_url = route_url.replace("OTL", user.make_one_time_link())
            if route["function"] == "POST":
                self.expectPostStatus(c, route_url, route["form"], route["template"], route["function"])
            elif route["function"] == "GET":
                self.expectGetStatus(c, route_url, route["template"], route["function"])
            if "logout" in route:
                print("\t\tNEEDS LOGOUT")
                c.get("/logout", follow_redirects=True)
            if "login" in route:
                print("\t\tNEEDS LOGIN")

        mock_get_patcher_get.stop()
        mock_get_patcher_post.stop()
        mock_get_patcher_smtp.stop()

    def test_not_logged_in_routes(self):
        with self.client as c:
            print()
            print("not_logged_in:")
            self.function_test(c, self.not_logged_in)

    def test_normal_user_logged_in_routes(self):
        with self.client as c:
            print()
            print("normal_user_logged_in:")
            self.function_test(c, self.normal_user_logged_in, user='testuser', password="Pa55wort")

    def test_super_user_logged_in_routes(self):
        with self.client as c:
            print()
            print("super_user_logged_in:")
            self.function_test(c, self.super_user_logged_in, user='superuser', password="Pa55wort")

if __name__ == "__main__":
    unittest.main()
