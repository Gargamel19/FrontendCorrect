import os
import unittest

from app import app, db, routes
from app.models import User


class UserTests(unittest.TestCase):

    ############################
    #    setup and teardown    #
    ############################

    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.config["BASEDIR"], 'test.db')
        self.app = app.test_client()
        db.create_all()

    # executed after each test
    def tearDown(self):
        db.session.remove()
        db.drop_all()

    ###############
    #    tests    #
    ###############

    def test_change_user_password(self):
        username = "FettarmQP"
        email = "trendelenburger19.04@googlemail.com"
        pw = "Pa55wort"
        neues_pw = "neues_Pa55wort"
        routes.add_user(username, email, pw, True)
        user_dummy = User.query.filter_by(username=username).first()
        user_dummy.set_password(neues_pw)
        user_dummy.save_user()
        self.assertTrue(user_dummy.check_password(neues_pw))
        user_dummy2 = User.query.filter_by(username=username).first()
        user_dummy2.set_password(pw)
        user_dummy2.save_user()
        self.assertTrue(user_dummy2.check_password(pw))

    def test_change_user_mail(self):
        username = "FettarmQP"
        email = "trendelenburger19.04@googlemail.com"
        pw = "Pa55wort"
        neue_mail = "dock.ferdi@googlemail.com"
        routes.add_user(username, email, pw, True)
        user_dummy = User.query.filter_by(username=username).first()
        user_dummy.set_mail(neue_mail)
        user_dummy.save_user()
        self.assertEqual(user_dummy.email, neue_mail)
        user_dummy2 = User.query.filter_by(username=username).first()
        user_dummy2.set_mail(email)
        user_dummy2.save_user()
        self.assertEqual(user_dummy2.email, email)


if __name__ == "__main__":
    unittest.main()
