"""Add user account status fields.

Revision ID: add_user_account_status
Revises: add_generic_reports
Create Date: 2026-03-13
"""

from alembic import op
import sqlalchemy as sa


revision = "add_user_account_status"
down_revision = "add_generic_reports"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
    )
    op.add_column(
        "users",
        sa.Column("deactivated_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.alter_column("users", "is_active", server_default=None)


def downgrade() -> None:
    op.drop_column("users", "deactivated_at")
    op.drop_column("users", "is_active")
