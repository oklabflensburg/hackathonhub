"""compatibility merge for legacy notification/user heads

Revision ID: merge_notif_user_heads
Revises: add_notification_masks, add_user_account_status
Create Date: 2026-03-14 17:50:00.000000

"""

revision = "merge_notif_user_heads"
down_revision = ("add_notification_masks", "add_user_account_status")
branch_labels = None
depends_on = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
