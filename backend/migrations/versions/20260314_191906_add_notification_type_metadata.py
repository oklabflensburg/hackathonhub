"""Add missing metadata fields to notification_types table

Revision ID: 20260314_191906
Revises: add_notification_masks
Create Date: 2026-03-14 19:19:06.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20260314_191906'
down_revision = 'add_notification_masks'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add help_text_key column for i18n translation keys
    op.add_column(
        'notification_types',
        sa.Column('help_text_key', sa.String(length=100), nullable=True)
    )

    # Add email_template column for email template paths
    op.add_column(
        'notification_types',
        sa.Column('email_template', sa.String(length=200), nullable=True)
    )

    # Update existing notification types with data from
    # notification_registry.py. This will be done in a separate
    # seed script, but we set up the columns here


def downgrade() -> None:
    # Remove the added columns
    op.drop_column('notification_types', 'email_template')
    op.drop_column('notification_types', 'help_text_key')
