import os
import unittest

os.environ.setdefault("DEBUG", "false")
os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")

from app.core.database import SessionLocal, engine  # noqa: E402
from app.domain.models import Base, User  # noqa: E402
from app.repositories.notification_repository import (  # noqa: E402
    NotificationDeliveryRepository,
    NotificationPreferenceRepository,
)
from app.services.in_app_notification_service import InAppNotificationService  # noqa: E402
from app.services.notification_preference_service import (  # noqa: E402
    notification_preference_service,
)
from app.services.notification_settings_service import (  # noqa: E402
    notification_settings_service,
)
from app.services.notification_service import NotificationService  # noqa: E402
from app.utils.notification_flags import CHANNEL_FLAGS  # noqa: E402
from app.utils.notification_mask_utils import has_flag  # noqa: E402


class NotificationRefactorTests(unittest.TestCase):
    def setUp(self):
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        self.db = SessionLocal()
        self.user = User(
            email="tester@example.com",
            username="tester",
            password_hash="secret",
        )
        self.db.add(self.user)
        self.db.commit()
        self.db.refresh(self.user)
        notification_preference_service.initialize_notification_types(self.db)

    def tearDown(self):
        self.db.close()

    def test_unknown_notification_type_fails_closed(self):
        self.assertFalse(
            notification_preference_service.should_send_notification(
                self.db, self.user.id, "does_not_exist", "email"
            )
        )

    def test_preference_disables_push_without_affecting_in_app(self):
        preference_repo = NotificationPreferenceRepository()
        settings = preference_repo.get_or_create_settings(
            self.db, user_id=self.user.id
        )
        preference_repo.update_settings_masks(
            self.db,
            preference=settings,
            types_mask=settings.types_mask_int,
            channels_mask=settings.channels_mask_int & ~CHANNEL_FLAGS["push"],
        )

        service = NotificationService()
        result = service.send_multi_channel_notification(
            self.db,
            notification_type="team_invitation",
            user_id=self.user.id,
            title="Invite",
            message="Join the team",
            channels=["push", "in_app"],
        )

        deliveries = service.get_user_notifications(self.db, self.user.id)[0].deliveries
        channels = {delivery.channel for delivery in deliveries}
        self.assertTrue(result["in_app"])
        self.assertNotIn("push", channels)
        self.assertIn("in_app", channels)

    def test_global_enabled_requires_all_type_flags(self):
        settings = notification_settings_service.get_settings(self.db, self.user.id)
        self.assertTrue(settings["global_enabled"])

        notification_settings_service.update_settings(
            self.db,
            self.user.id,
            {"types": {"team_invitation": {"enabled": False}}},
        )
        updated = notification_settings_service.get_settings(self.db, self.user.id)
        self.assertFalse(updated["global_enabled"])
        self.assertFalse(updated["categories"]["team"]["enabled"])

    def test_masks_are_persisted_as_strings(self):
        notification_settings_service.update_settings(
            self.db,
            self.user.id,
            {"channels": {"push": False}},
        )
        preference = NotificationPreferenceRepository().get_by_user_id(
            self.db, self.user.id
        )
        self.assertIsInstance(preference.types_mask, str)
        self.assertIsInstance(preference.channels_mask, str)
        self.assertFalse(has_flag(preference.channels_mask_int, CHANNEL_FLAGS["push"]))

    def test_notification_persists_one_logical_record_with_deliveries(self):
        service = NotificationService()
        service.send_multi_channel_notification(
            self.db,
            notification_type="system_announcement",
            user_id=self.user.id,
            title="Title",
            message="Body",
            channels=["in_app"],
        )

        notifications = service.get_user_notifications(self.db, self.user.id)
        self.assertEqual(len(notifications), 1)
        self.assertEqual(notifications[0].notification_type, "system_announcement")
        self.assertEqual(len(notifications[0].deliveries), 1)
        self.assertEqual(notifications[0].deliveries[0].channel, "in_app")
        self.assertEqual(notifications[0].deliveries[0].status, "delivered")

    def test_in_app_service_list_and_mark_read(self):
        service = InAppNotificationService()
        notification = service.store_notification(
            self.db,
            user_id=self.user.id,
            title="Hello",
            body="World",
            notification_type="system_announcement",
            data={"metadata": {"source": "test"}},
        )

        notifications = service.get_user_notifications(self.db, self.user.id)
        self.assertEqual(len(notifications), 1)
        self.assertEqual(notifications[0].id, notification.id)
        self.assertTrue(service.mark_as_read(self.db, notification.id, self.user.id))
        refreshed = NotificationService().get_user_notifications(self.db, self.user.id)[0]
        self.assertIsNotNone(refreshed.read_at)

    def test_delivery_repository_tracks_status_updates(self):
        service = NotificationService()
        service.send_multi_channel_notification(
            self.db,
            notification_type="system_announcement",
            user_id=self.user.id,
            title="Hello",
            message="World",
            channels=["in_app"],
        )
        notification = service.get_user_notifications(self.db, self.user.id)[0]
        delivery_repo = NotificationDeliveryRepository()
        delivery = delivery_repo.get_by_notification(self.db, notification.id)[0]
        self.assertEqual(delivery.attempt_count, 1)
        self.assertEqual(delivery.status, "delivered")


if __name__ == "__main__":
    unittest.main()
