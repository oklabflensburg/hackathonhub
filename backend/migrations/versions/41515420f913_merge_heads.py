"""merge heads

Revision ID: 41515420f913
Revises: add_view_count_to_hackathons, add_vote_score_to_comments
Create Date: 2026-02-24 17:40:56.848864

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '41515420f913'
down_revision = ('add_view_count_to_hackathons', 'add_vote_score_to_comments')
branch_labels = None
depends_on = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
