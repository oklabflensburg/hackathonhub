"""merge remaining heads

Revision ID: 9f5ab90ded12
Revises: 2e3056024a16, add_refresh_token_persistence, add_notification_enhancements
Create Date: 2026-03-13 13:15:00.000000

"""


# revision identifiers, used by Alembic.
revision = '9f5ab90ded12'
down_revision = (
    '2e3056024a16',
    'add_refresh_token_persistence',
    'add_notification_enhancements',
)
branch_labels = None
depends_on = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
