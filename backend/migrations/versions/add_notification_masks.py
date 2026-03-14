"""add notification masks

Revision ID: add_notification_masks
Revises: drop_legacy_notification_cols
Create Date: 2026-03-14 11:30:00.000000

"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect, text


revision = "add_notification_masks"
down_revision = "drop_legacy_notification_cols"
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

    preference_columns = {
        column["name"]
        for column in inspector.get_columns("user_notification_preferences")
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

    type_columns = {
        column["name"] for column in inspector.get_columns("notification_types")
    }
    if "help_text" not in type_columns:
        op.add_column("notification_types", sa.Column("help_text", sa.Text(), nullable=True))
    if "type_flag" not in type_columns:
        op.add_column("notification_types", sa.Column("type_flag", sa.String(length=255), nullable=True))
    if "sort_order" not in type_columns:
        op.add_column(
            "notification_types",
            sa.Column("sort_order", sa.Integer(), nullable=False, server_default="0"),
        )

    _backfill_notification_types(bind)
    _backfill_masks(bind, preference_columns)

    with op.batch_alter_table("user_notification_preferences") as batch_op:
        if "notification_type" in preference_columns:
            batch_op.drop_column("notification_type")
        if "channel" in preference_columns:
            batch_op.drop_column("channel")
        if "enabled" in preference_columns:
            batch_op.drop_column("enabled")

    index_names = {
        index["name"] for index in inspector.get_indexes("user_notification_preferences")
    }
    if "ix_user_notification_preferences_user_id" in index_names:
        op.drop_index(
            "ix_user_notification_preferences_user_id",
            table_name="user_notification_preferences",
        )

    unique_constraints = {
        constraint["name"]
        for constraint in inspector.get_unique_constraints("user_notification_preferences")
        if constraint["name"]
    }
    if "_user_notification_channel_uc" in unique_constraints:
        with op.batch_alter_table("user_notification_preferences") as batch_op:
            batch_op.drop_constraint("_user_notification_channel_uc", type_="unique")

    with op.batch_alter_table("user_notification_preferences") as batch_op:
        batch_op.alter_column("types_mask", nullable=False)
        batch_op.alter_column("channels_mask", nullable=False)
        batch_op.create_unique_constraint(
            "uq_user_notification_preferences_user", ["user_id"]
        )


def downgrade() -> None:
    with op.batch_alter_table("user_notification_preferences") as batch_op:
        batch_op.drop_constraint("uq_user_notification_preferences_user", type_="unique")
        batch_op.add_column(sa.Column("enabled", sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column("channel", sa.String(length=20), nullable=True))
        batch_op.add_column(sa.Column("notification_type", sa.String(length=50), nullable=True))

    op.drop_column("user_notification_preferences", "types_mask")
    op.drop_column("user_notification_preferences", "channels_mask")
    op.drop_column("notification_types", "help_text")
    op.drop_column("notification_types", "type_flag")
    op.drop_column("notification_types", "sort_order")


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
                    type_flag = :type_flag,
                    sort_order = :sort_order
                WHERE id = :id
                """
            ),
            {
                "id": row.id,
                "type_flag": str(1 << index),
                "sort_order": index,
            },
        )


def _backfill_masks(bind, preference_columns) -> None:
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
    existing_users = [
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
        for user_id in existing_users
    }

    if {"notification_type", "channel", "enabled"}.issubset(preference_columns):
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
        primary_id = bind.execute(
            text(
                """
                SELECT id
                FROM user_notification_preferences
                WHERE user_id = :user_id
                ORDER BY id ASC
                LIMIT 1
                """
            ),
            {"user_id": user_id},
        ).scalar_one()
        bind.execute(
            text(
                """
                UPDATE user_notification_preferences
                SET types_mask = :types_mask,
                    channels_mask = :channels_mask
                WHERE id = :id
                """
            ),
            {
                "id": primary_id,
                "types_mask": str(user_data["types_mask"]),
                "channels_mask": str(user_data["channels_mask"]),
            },
        )
        bind.execute(
            text(
                """
                DELETE FROM user_notification_preferences
                WHERE user_id = :user_id AND id <> :id
                """
            ),
            {"user_id": user_id, "id": primary_id},
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
