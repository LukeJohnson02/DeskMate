import unittest
from fastapi.testclient import TestClient

from Tests.populate_db import populate_db
from main import app

client = TestClient(app)


class AuthTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Populate the test database once before all tests
        populate_db()

    def test_login_success(self):
        response = client.post(
            "/auth/login",
            data={"username": "user1@example.com", "password": "password123"},
        )
        self.assertEqual(response.status_code, 200)
        # Optionally, check the response content for tokens, user info, etc.

    def test_login_fail_wrong_password(self):
        response = client.post(
            "/auth/login",
            data={"username": "user1@example.com", "password": "wrongpass"},
        )
        self.assertEqual(response.status_code, 401)


if __name__ == "__main__":
    unittest.main()
