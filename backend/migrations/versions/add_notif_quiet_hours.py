"""add quiet hours to notification preferences

Revision ID: add_notif_quiet_hours
Revises: fix_notif_mask_schema
Create Date: 2026-03-14 18:10:00.000000

"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect, text
from sqlalchemy.dialects import postgresql


revision = "add_notif_quiet_hours"
down_revision = "fix_notif_mask_schema"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = inspect(bind)
    columns = {
        column["name"]
        for column in inspector.get_columns("user_notification_preferences")
    }

    if "quiet_hours" not in columns:
        op.add_column(
            "user_notification_preferences",
            sa.Column(
                "quiet_hours",
                sa.JSON().with_variant(postgresql.JSONB, "postgresql"),
                nullable=True,
            ),
        )

    bind.execute(
        text(
            """
            UPDATE user_notification_preferences
            SET quiet_hours = COALESCE(
                quiet_hours,
                '{"enabled": false, "start": "22:00", "end": "08:00", "days": []}'::jsonb
            )
            """
        )
    )


def downgrade() -> None:
    bind = op.get_bind()
    inspector = inspect(bind)
    columns = {
        column["name"]
        for column in inspector.get_columns("user_notification_preferences")
    }
    if "quiet_hours" in columns:
        op.drop_column("user_notification_preferences", "quiet_hours")
