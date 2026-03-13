"""add notification delivery table

Revision ID: add_notification_delivery_table
Revises: 9f5ab90ded12
Create Date: 2026-03-13 15:30:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect, text


# revision identifiers, used by Alembic.
revision = "add_notification_delivery_table"
down_revision = "9f5ab90ded12"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = inspect(bind)
    existing_tables = set(inspector.get_table_names())

    if "notification_deliveries" not in existing_tables:
        op.create_table(
            "notification_deliveries",
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("notification_id", sa.Integer(), nullable=False),
            sa.Column("channel", sa.String(length=20), nullable=False),
            sa.Column("status", sa.String(length=20), nullable=False, server_default="pending"),
            sa.Column("error", sa.Text(), nullable=True),
            sa.Column("provider_message_id", sa.String(length=255), nullable=True),
            sa.Column("attempt_count", sa.Integer(), nullable=False, server_default="0"),
            sa.Column("last_attempt_at", sa.DateTime(timezone=True), nullable=True),
            sa.Column("delivered_at", sa.DateTime(timezone=True), nullable=True),
            sa.Column(
                "created_at",
                sa.DateTime(timezone=True),
                server_default=sa.text("now()"),
                nullable=False,
            ),
            sa.ForeignKeyConstraint(
                ["notification_id"], ["user_notifications.id"], ondelete="CASCADE"
            ),
            sa.PrimaryKeyConstraint("id"),
        )
        op.create_index(
            "ix_notification_deliveries_notification_id",
            "notification_deliveries",
            ["notification_id"],
        )
        op.create_index(
            "ix_notification_deliveries_channel_status",
            "notification_deliveries",
            ["channel", "status"],
        )

    notification_columns = {
        column["name"] for column in inspector.get_columns("user_notifications")
    }
    channel_column = None
    if "channels" in notification_columns:
        channel_column = "channels"
    elif "channels_sent" in notification_columns:
        channel_column = "channels_sent"

    status_column = "status" if "status" in notification_columns else None
    delivered_column = (
        "delivered_at" if "delivered_at" in notification_columns else None
    )

    rows = bind.execute(
        text(
            "SELECT id"
            + (f", {channel_column}" if channel_column else "")
            + (f", {status_column}" if status_column else "")
            + (f", {delivered_column}" if delivered_column else "")
            + " FROM user_notifications"
        )
    ).fetchall()

    insert_sql = text(
        """
        INSERT INTO notification_deliveries
            (notification_id, channel, status, delivered_at, created_at)
        VALUES
            (:notification_id, :channel, :status, :delivered_at, now())
        """
    )

    for row in rows:
        mapping = row._mapping
        notification_id = mapping["id"]
        channels_value = mapping.get(channel_column) if channel_column else None
        status_value = mapping.get(status_column) if status_column else None
        delivered_at = mapping.get(delivered_column) if delivered_column else None

        channels = _parse_channels(channels_value)
        if not channels:
            channels = ["in_app"]

        for channel in channels:
            bind.execute(
                insert_sql,
                {
                    "notification_id": notification_id,
                    "channel": channel,
                    "status": status_value or "delivered",
                    "delivered_at": delivered_at,
                },
            )


def downgrade() -> None:
    op.drop_index(
        "ix_notification_deliveries_channel_status",
        table_name="notification_deliveries",
    )
    op.drop_index(
        "ix_notification_deliveries_notification_id",
        table_name="notification_deliveries",
    )
    op.drop_table("notification_deliveries")


def _parse_channels(value):
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item) for item in value if item]
    if isinstance(value, str):
        text_value = value.strip()
        if not text_value:
            return []
        if text_value.startswith("[") and text_value.endswith("]"):
            text_value = text_value.strip("[]").replace('"', "")
        if text_value.startswith("{") and text_value.endswith("}"):
            return []
        return [channel.strip() for channel in text_value.split(",") if channel.strip()]
    return []
