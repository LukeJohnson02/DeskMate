import unittest
from fastapi.testclient import TestClient

from Tests.populate_db import populate_db
from main import app

client = TestClient(app)


class TicketTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Populate database once before all tests
        populate_db()

        # Login as regular user
        response = client.post(
            "/auth/login",
            data={"username": "user1@example.com", "password": "password123"},
        )
        cls.user1_token = response.json().get("access_token")
        cls.user1_headers = {"Authorization": f"Bearer {cls.user1_token}"}

        # Login as admin
        response = client.post(
            "/auth/login",
            data={"username": "admin1@example.com", "password": "adminpass123"},
        )
        cls.admin_token = response.json().get("access_token")
        cls.admin_headers = {"Authorization": f"Bearer {cls.admin_token}"}

        # Create a ticket as user1 to test ownership related cases
        create_response = client.post(
            "/tickets/",
            params={
                "title": "Test Ticket",
                "description": "Test description",
                "category_id": 1,
            },
            headers=cls.user1_headers,
        )
        assert create_response.status_code == 200
        cls.ticket_id = create_response.json().get("id")

    def test_read_tickets(self):
        # User can read tickets
        response = client.get("/tickets/", headers=self.user1_headers)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.json(), list))

    def test_read_single_ticket_owner(self):
        # Owner can read their ticket
        response = client.get(f"/tickets/{self.ticket_id}", headers=self.user1_headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("id"), self.ticket_id)

    def test_read_single_ticket_not_owner(self):
        # Admin can read any ticket (assuming admin role)
        response = client.get(f"/tickets/{self.ticket_id}", headers=self.admin_headers)
        self.assertEqual(response.status_code, 200)

    def test_update_ticket_owner(self):
        # Owner updates their ticket
        response = client.put(
            f"/tickets/{self.ticket_id}",
            params={
                "title": "Updated Title",
                "description": "Updated description",
                "status": "IN_PROGRESS",
            },
            headers=self.user1_headers,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("title"), "Updated Title")

    def test_update_ticket_not_owner(self):
        # Another user (not owner) tries to update ticket - should fail with 403
        # Create login for user2
        response = client.post(
            "/auth/login",
            data={"username": "user2@example.com", "password": "password123"},
        )
        token = response.json().get("access_token")
        headers = {"Authorization": f"Bearer {token}"}

        response = client.put(
            f"/tickets/{self.ticket_id}",
            params={
                "title": "Malicious Update",
                "description": "Malicious description",
                "status": "CLOSED",
            },
            headers=headers,
        )
        self.assertEqual(response.status_code, 403)

    def test_update_ticket_admin(self):
        # Admin updates any ticket
        response = client.put(
            f"/tickets/{self.ticket_id}",
            params={
                "title": "Admin Updated Title",
                "description": "Admin updated description",
                "status": "CLOSED",
            },
            headers=self.admin_headers,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("title"), "Admin Updated Title")

    def test_delete_ticket_owner(self):
        # Owner deletes their ticket
        # First create a new ticket for delete test
        create_response = client.post(
            "/tickets/",
            params={
                "title": "Delete Ticket",
                "description": "Delete description",
                "category_id": 1,
            },
            headers=self.user1_headers,
        )
        ticket_id = create_response.json().get("id")

        response = client.delete(f"/tickets/{ticket_id}", headers=self.user1_headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("detail"), "Ticket deleted successfully")

    def test_delete_ticket_not_owner(self):
        # Another user tries to delete ticket (should be forbidden)
        # Create login for user2
        response = client.post(
            "/auth/login",
            data={"username": "user2@example.com", "password": "password123"},
        )
        token = response.json().get("access_token")
        headers = {"Authorization": f"Bearer {token}"}

        response = client.delete(f"/tickets/{self.ticket_id}", headers=headers)
        self.assertEqual(response.status_code, 403)

    def test_delete_ticket_admin(self):
        # Admin deletes a ticket
        # First create a new ticket by user1
        create_response = client.post(
            "/tickets/",
            params={
                "title": "Admin Delete Ticket",
                "description": "Admin delete description",
                "category_id": 1,
            },
            headers=self.user1_headers,
        )
        ticket_id = create_response.json().get("id")

        response = client.delete(f"/tickets/{ticket_id}", headers=self.admin_headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("detail"), "Ticket deleted successfully")


if __name__ == "__main__":
    unittest.main()
