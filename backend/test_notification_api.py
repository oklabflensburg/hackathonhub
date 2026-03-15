import os
import unittest

os.environ.setdefault("DEBUG", "false")
os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")

from fastapi.testclient import TestClient  # noqa: E402

from app.core.auth import create_tokens  # noqa: E402
from app.core.database import SessionLocal, engine  # noqa: E402
from app.domain.models import Base, User  # noqa: E402
from app.main import app  # noqa: E402
from app.services.notification_preference_service import (  # noqa: E402
    notification_preference_service,
)
from app.services.notification_service import NotificationService  # noqa: E402


class NotificationApiTests(unittest.TestCase):
    def setUp(self):
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        self.db = SessionLocal()
        self.user = User(
            email="api@example.com",
            username="apiuser",
            password_hash="secret",
            email_verified=True,
        )
        self.db.add(self.user)
        self.db.commit()
        self.db.refresh(self.user)
        notification_preference_service.initialize_notification_types(self.db)
        self.client = TestClient(app)
        access_token = create_tokens(self.user.id, self.user.username)["access_token"]
        self.headers = {"Authorization": f"Bearer {access_token}"}

    def tearDown(self):
        self.client.close()
        self.db.close()

    def test_notifications_list_and_read_flow(self):
        service = NotificationService()
        service.send_multi_channel_notification(
            self.db,
            notification_type="system_announcement",
            user_id=self.user.id,
            title="Hello",
            message="World",
            channels=["in_app"],
        )

        response = self.client.get("/api/notifications", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(len(payload), 1)
        self.assertEqual(payload[0]["notification_type"], "system_announcement")
        self.assertEqual(payload[0]["type"], "system_announcement")
        self.assertEqual(payload[0]["deliveries"][0]["channel"], "in_app")

        notification_id = payload[0]["id"]
        read_response = self.client.post(
            f"/api/notifications/{notification_id}/read",
            headers=self.headers,
        )
        self.assertEqual(read_response.status_code, 200)

        refreshed = self.client.get("/api/notifications", headers=self.headers).json()
        self.assertIsNotNone(refreshed[0]["read_at"])

    def test_in_app_create_list_and_delete(self):
        create_response = self.client.post(
            "/api/notifications/in-app",
            headers=self.headers,
            json={
                "title": "Title",
                "message": "Body",
                "type": "system_announcement",
                "priority": "high",
                "action_url": "/notifications",
                "metadata": {"source": "api-test"},
            },
        )
        self.assertEqual(create_response.status_code, 201)
        created = create_response.json()
        self.assertEqual(created["notification_type"], "system_announcement")
        self.assertEqual(created["priority"], "high")
        self.assertEqual(created["action_url"], "/notifications")

        list_response = self.client.get(
            "/api/notifications/in-app/list",
            headers=self.headers,
        )
        self.assertEqual(list_response.status_code, 200)
        listed = list_response.json()
        self.assertEqual(listed["total"], 1)
        self.assertEqual(listed["notifications"][0]["metadata"]["source"], "api-test")

        unread_response = self.client.get(
            "/api/notifications/in-app/unread-count",
            headers=self.headers,
        )
        self.assertEqual(unread_response.status_code, 200)
        self.assertEqual(unread_response.json()["count"], 1)

        notification_id = listed["notifications"][0]["id"]
        delete_response = self.client.delete(
            f"/api/notifications/in-app/{notification_id}",
            headers=self.headers,
        )
        self.assertEqual(delete_response.status_code, 200)

        final_list = self.client.get(
            "/api/notifications/in-app/list",
            headers=self.headers,
        ).json()
        self.assertEqual(final_list["total"], 0)

    def test_preferences_endpoint_returns_masks_and_derived_state(self):
        response = self.client.get(
            "/api/notifications/preferences",
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertIn("masks", payload)
        self.assertTrue(payload["global_enabled"])

        update_response = self.client.put(
            "/api/notifications/preferences",
            headers=self.headers,
            json={"types": {"team_invitation": {"enabled": False}}},
        )
        self.assertEqual(update_response.status_code, 200)

        refreshed = self.client.get(
            "/api/notifications/preferences",
            headers=self.headers,
        ).json()
        self.assertFalse(refreshed["global_enabled"])
        self.assertFalse(refreshed["categories"]["team"]["enabled"])


if __name__ == "__main__":
    unittest.main()
