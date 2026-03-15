"""add user platform preference columns

Revision ID: add_user_platform_prefs
Revises: merge_notif_meta_quiet
Create Date: 2026-03-15 12:40:00.000000

"""

from alembic import op
import sqlalchemy as sa


revision = "add_user_platform_prefs"
down_revision = "merge_notif_meta_quiet"
branch_labels = None
depends_on = None


def _column_names(bind, table_name: str) -> set[str]:
    inspector = sa.inspect(bind)
    return {column["name"] for column in inspector.get_columns(table_name)}


def upgrade() -> None:
    bind = op.get_bind()
    columns = _column_names(bind, "users")

    additions = [
        ("theme", sa.Column("theme", sa.String(length=16), nullable=False, server_default="system")),
        ("language", sa.Column("language", sa.String(length=8), nullable=False, server_default="en")),
        ("timezone", sa.Column("timezone", sa.String(length=64), nullable=False, server_default="UTC")),
        ("date_format", sa.Column("date_format", sa.String(length=16), nullable=False, server_default="YYYY-MM-DD")),
        ("time_format", sa.Column("time_format", sa.String(length=8), nullable=False, server_default="24h")),
        ("notifications_sound", sa.Column("notifications_sound", sa.Boolean(), nullable=False, server_default=sa.true())),
        ("reduce_animations", sa.Column("reduce_animations", sa.Boolean(), nullable=False, server_default=sa.false())),
        ("compact_mode", sa.Column("compact_mode", sa.Boolean(), nullable=False, server_default=sa.false())),
        ("default_view_hackathons", sa.Column("default_view_hackathons", sa.String(length=16), nullable=False, server_default="grid")),
        ("default_view_projects", sa.Column("default_view_projects", sa.String(length=16), nullable=False, server_default="grid")),
        ("default_view_notifications", sa.Column("default_view_notifications", sa.String(length=24), nullable=False, server_default="grouped")),
    ]

    for name, column in additions:
        if name not in columns:
            op.add_column("users", column)


def downgrade() -> None:
    bind = op.get_bind()
    columns = _column_names(bind, "users")

    for name in [
        "default_view_notifications",
        "default_view_projects",
        "default_view_hackathons",
        "compact_mode",
        "reduce_animations",
        "notifications_sound",
        "time_format",
        "date_format",
        "timezone",
        "language",
        "theme",
    ]:
        if name in columns:
            op.drop_column("users", name)
