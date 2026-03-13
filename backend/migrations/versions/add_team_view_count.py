"""add team view count

Revision ID: add_team_view_count
Revises: drop_legacy_notification_cols
Create Date: 2026-03-13 17:20:00.000000
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'add_team_view_count'
down_revision: Union[str, None] = 'drop_legacy_notification_cols'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('teams', sa.Column('view_count', sa.Integer(), nullable=False, server_default='0'))
    op.alter_column('teams', 'view_count', server_default=None)


def downgrade() -> None:
    op.drop_column('teams', 'view_count')
