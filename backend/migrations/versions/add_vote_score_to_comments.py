"""Add vote_score column to comments table

Revision ID: add_vote_score_to_comments
Revises: add_user_agent_to_push
Create Date: 2026-02-23 07:48:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_vote_score_to_comments'
down_revision = 'add_user_agent_to_push'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add vote_score column to comments table
    op.add_column('comments',
                  sa.Column('vote_score', sa.Integer(),
                            nullable=True, server_default='0'))
    # Update existing rows to set vote_score = upvote_count - downvote_count
    # This is optional but ensures consistency
    op.execute("""
        UPDATE comments 
        SET vote_score = upvote_count - downvote_count 
        WHERE vote_score IS NULL
    """)


def downgrade() -> None:
    # Remove vote_score column from comments table
    op.drop_column('comments', 'vote_score')