"""merge notification metadata and quiet hours heads

Revision ID: merge_notif_meta_quiet
Revises: 20260314_191906, add_notif_quiet_hours
Create Date: 2026-03-15 10:15:00.000000

"""

revision = "merge_notif_meta_quiet"
down_revision = ("20260314_191906", "add_notif_quiet_hours")
branch_labels = None
depends_on = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
