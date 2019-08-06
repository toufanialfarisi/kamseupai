from apps import app, db
from apps.auth.models import User
import unittest


class MonolitikTesting(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        pass

    @classmethod
    def tearDownClass(self):
        pass

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_index(self):
        result = self.app.get("/")
        self.assertEqual(result.status_code, 200)

    def test_login(self):
        user = User(
            username="admin2019", email="toufani15@gmail.com", password="admin2019"
        )
        result = self.app.post("/login")
        self.assertEqual(result.status_code, 200)


if __name__ == "__main__":
    unittest.main()
