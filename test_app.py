import apps
from apps.auth.models import User
import unittest
from flask import request, url_for
from flask_login import (
    UserMixin,
    login_user,
    logout_user,
    current_user,
    login_required,
    LoginManager,
)
import os


class MonolitikTesting(unittest.TestCase):
    def setUp(self):
        self.app = apps.app.test_client()
        self.app.testing = True
        apps.app.config.from_object("config.TestingConfig")
        apps.app.config["SECRET_KEY"] = "kamseupaiTesting2019"
        apps.db.create_all()
        login_manager = LoginManager()
        login_manager.init_app(apps.app)

    def tearDown(self):
        apps.db.session.remove()
        apps.db.drop_all()

    def test_index(self):
        result = self.app.get("/")
        self.assertEqual(result.status_code, 200)

    def test_create_user(
        self,
        username="toufani alfarisi",
        email="toufani1515@gmail.com",
        password="113966755098006852222alfarisi",
        foto_user=None,
    ):
        user = User(username, email, password, foto_user)
        apps.db.session.add(user)
        apps.db.session.commit()
        result = self.app.post("/login")
        self.assertEqual(result.status_code, 200)

    def test_login_user(
        self,
        username="toufani alfarisi",
        email="toufani1515@gmail.com",
        password="113966755098006852222alfarisi",
        foto_user=None,
    ):
        result = self.app.post(
            "/login",
            data=dict(
                username=username, email=email, password=password, foto_user=foto_user
            ),
            follow_redirects=True,
        )
        self.assertEqual(result.status_code, 200)


if __name__ == "__main__":
    unittest.main()
