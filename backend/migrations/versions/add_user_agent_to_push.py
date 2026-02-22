"""Add user_agent column to push_subscriptions table

Revision ID: add_user_agent_to_push
Revises: add_notification_tables, fix_refresh_tokens_auto_inc
Create Date: 2026-02-21 18:01:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_user_agent_to_push'
down_revision = ('add_notification_tables', 'fix_refresh_tokens_auto_inc')
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add user_agent column to push_subscriptions table
    op.add_column('push_subscriptions',
                  sa.Column('user_agent', sa.Text(), nullable=True))


def downgrade() -> None:
    # Remove user_agent column from push_subscriptions table
    op.drop_column('push_subscriptions', 'user_agent')