"""fix notification mask schema after legacy merge state

Revision ID: fix_notif_mask_schema
Revises: merge_notif_masks_user_status
Create Date: 2026-03-14 17:48:00.000000

"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect, text


revision = "fix_notif_mask_schema"
down_revision = "merge_notif_masks_user_status"
branch_labels = None
depends_on = None


CHANNEL_BITS = {
    "email": 1 << 0,
    "push": 1 << 1,
    "in_app": 1 << 2,
}


def upgrade() -> None:
    bind = op.get_bind()
    inspector = inspect(bind)

    notification_type_columns = {
        column["name"] for column in inspector.get_columns("notification_types")
    }
    if "help_text" not in notification_type_columns:
        op.add_column("notification_types", sa.Column("help_text", sa.Text(), nullable=True))
    if "type_flag" not in notification_type_columns:
        op.add_column("notification_types", sa.Column("type_flag", sa.String(length=255), nullable=True))
    if "sort_order" not in notification_type_columns:
        op.add_column(
            "notification_types",
            sa.Column("sort_order", sa.Integer(), nullable=False, server_default="0"),
        )

    preference_columns = {
        column["name"] for column in inspector.get_columns("user_notification_preferences")
    }
    if "types_mask" not in preference_columns:
        op.add_column(
            "user_notification_preferences",
            sa.Column("types_mask", sa.String(length=255), nullable=True),
        )
    if "channels_mask" not in preference_columns:
        op.add_column(
            "user_notification_preferences",
            sa.Column("channels_mask", sa.String(length=255), nullable=True),
        )

    _backfill_notification_types(bind)
    _backfill_preferences(bind, preference_columns)


def downgrade() -> None:
    pass


def _backfill_notification_types(bind) -> None:
    rows = bind.execute(
        text(
            "SELECT id, type_key, description FROM notification_types ORDER BY id ASC"
        )
    ).fetchall()
    for index, row in enumerate(rows):
        bind.execute(
            text(
                """
                UPDATE notification_types
                SET help_text = COALESCE(help_text, description),
                    type_flag = COALESCE(type_flag, :type_flag),
                    sort_order = CASE WHEN sort_order IS NULL THEN :sort_order ELSE sort_order END
                WHERE id = :id
                """
            ),
            {
                "id": row.id,
                "type_flag": str(1 << index),
                "sort_order": index,
            },
        )


def _backfill_preferences(bind, existing_columns) -> None:
    type_rows = bind.execute(
        text(
            "SELECT type_key, id FROM notification_types ORDER BY sort_order ASC, id ASC"
        )
    ).fetchall()
    type_bits = {
        row.type_key: 1 << index
        for index, row in enumerate(type_rows)
    }
    all_types_mask = sum(type_bits.values())
    all_channels_mask = sum(CHANNEL_BITS.values())

    user_ids = [
        row.user_id
        for row in bind.execute(
            text(
                "SELECT DISTINCT user_id FROM user_notification_preferences ORDER BY user_id ASC"
            )
        ).fetchall()
    ]
    aggregated = {
        user_id: {
            "types_mask": all_types_mask,
            "channels_mask": all_channels_mask,
        }
        for user_id in user_ids
    }

    if {"notification_type", "channel", "enabled"}.issubset(existing_columns):
        rows = bind.execute(
            text(
                """
                SELECT user_id, notification_type, channel, enabled
                FROM user_notification_preferences
                ORDER BY user_id ASC, id ASC
                """
            )
        ).fetchall()
        for row in rows:
            user_data = aggregated.setdefault(
                row.user_id,
                {"types_mask": all_types_mask, "channels_mask": all_channels_mask},
            )
            type_flag = type_bits.get(row.notification_type)
            channel_flag = CHANNEL_BITS.get(row.channel)
            if type_flag is None or channel_flag is None:
                continue
            if row.enabled:
                user_data["channels_mask"] |= channel_flag
            else:
                user_data["types_mask"] &= ~type_flag

    for user_id, user_data in aggregated.items():
        bind.execute(
            text(
                """
                UPDATE user_notification_preferences
                SET types_mask = COALESCE(types_mask, :types_mask),
                    channels_mask = COALESCE(channels_mask, :channels_mask)
                WHERE user_id = :user_id
                """
            ),
            {
                "user_id": user_id,
                "types_mask": str(user_data["types_mask"]),
                "channels_mask": str(user_data["channels_mask"]),
            },
        )

    bind.execute(
        text(
            """
            UPDATE user_notification_preferences
            SET types_mask = COALESCE(types_mask, :types_mask),
                channels_mask = COALESCE(channels_mask, :channels_mask)
            """
        ),
        {
            "types_mask": str(all_types_mask),
            "channels_mask": str(all_channels_mask),
        },
    )
