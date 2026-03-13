"""drop legacy notification columns

Revision ID: drop_legacy_notification_cols
Revises: add_notification_delivery_table
Create Date: 2026-03-13 16:15:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect


revision = "drop_legacy_notification_cols"
down_revision = "add_notification_delivery_table"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = inspect(bind)

    if "notification_preferences" in inspector.get_table_names():
        index_names = {
            index["name"]
            for index in inspector.get_indexes("notification_preferences")
        }
        if "ix_notification_preferences_user_id" in index_names:
            op.drop_index(
                "ix_notification_preferences_user_id",
                table_name="notification_preferences",
            )
        op.drop_table("notification_preferences")

    columns = {column["name"] for column in inspector.get_columns("user_notifications")}
    for column_name in (
        "channels",
        "channels_sent",
        "status",
        "priority",
        "sent_at",
        "delivered_at",
        "expires_at",
        "action_url",
    ):
        if column_name in columns:
            op.drop_column("user_notifications", column_name)


def downgrade() -> None:
    op.add_column(
        "user_notifications",
        sa.Column("action_url", sa.Text(), nullable=True),
    )
    op.add_column(
        "user_notifications",
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.add_column(
        "user_notifications",
        sa.Column("delivered_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.add_column(
        "user_notifications",
        sa.Column("sent_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.add_column(
        "user_notifications",
        sa.Column("priority", sa.String(length=20), nullable=True),
    )
    op.add_column(
        "user_notifications",
        sa.Column("status", sa.String(length=50), nullable=True),
    )
    op.add_column(
        "user_notifications",
        sa.Column("channels_sent", sa.String(length=100), nullable=True),
    )

    op.create_table(
        "notification_preferences",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("channels", sa.JSON(), nullable=True),
        sa.Column("notification_types", sa.JSON(), nullable=True),
        sa.Column("quiet_hours", sa.JSON(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id"),
    )
    op.create_index(
        "ix_notification_preferences_user_id",
        "notification_preferences",
        ["user_id"],
    )
