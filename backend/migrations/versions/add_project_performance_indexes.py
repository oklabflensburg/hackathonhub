"""add_project_performance_indexes

Revision ID: add_project_performance_indexes
Revises: 41515420f913
Create Date: 2026-02-25 16:23:00.000000

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = 'add_project_performance_indexes'
down_revision = '41515420f913'
branch_labels = None
depends_on = None


def upgrade():
    # Create indexes for performance optimization
    op.create_index(
        'idx_projects_is_public_created_at',
        'projects',
        ['is_public', 'created_at'],
        unique=False
    )
    op.create_index(
        'idx_projects_owner_id_created_at',
        'projects',
        ['owner_id', 'created_at'],
        unique=False
    )
    op.create_index(
        'idx_projects_hackathon_id_created_at',
        'projects',
        ['hackathon_id', 'created_at'],
        unique=False
    )
    op.create_index(
        'idx_projects_team_id_created_at',
        'projects',
        ['team_id', 'created_at'],
        unique=False
    )

    # Create index for technologies search
    # Using regular B-tree index for ILIKE searches with pattern matching
    op.create_index(
        'idx_projects_technologies',
        'projects',
        ['technologies'],
        unique=False
    )

    # Create indexes for vote counts
    op.create_index(
        'idx_projects_upvote_count',
        'projects',
        ['upvote_count'],
        unique=False
    )
    op.create_index(
        'idx_projects_downvote_count',
        'projects',
        ['downvote_count'],
        unique=False
    )
    op.create_index(
        'idx_projects_vote_score',
        'projects',
        ['vote_score'],
        unique=False
    )

    # Create indexes for views and comments
    op.create_index(
        'idx_projects_view_count',
        'projects',
        ['view_count'],
        unique=False
    )
    op.create_index(
        'idx_projects_comment_count',
        'projects',
        ['comment_count'],
        unique=False
    )

    # Create index for votes table
    op.create_index(
        'idx_votes_user_project',
        'votes',
        ['user_id', 'project_id'],
        unique=False
    )
    op.create_index(
        'idx_votes_project_vote_type',
        'votes',
        ['project_id', 'vote_type'],
        unique=False
    )


def downgrade():
    # Drop all created indexes
    op.drop_index(
        'idx_projects_is_public_created_at',
        table_name='projects'
    )
    op.drop_index(
        'idx_projects_owner_id_created_at',
        table_name='projects'
    )
    op.drop_index(
        'idx_projects_hackathon_id_created_at',
        table_name='projects'
    )
    op.drop_index(
        'idx_projects_team_id_created_at',
        table_name='projects'
    )
    op.drop_index(
        'idx_projects_technologies',
        table_name='projects'
    )
    op.drop_index(
        'idx_projects_upvote_count',
        table_name='projects'
    )
    op.drop_index(
        'idx_projects_downvote_count',
        table_name='projects'
    )
    op.drop_index(
        'idx_projects_vote_score',
        table_name='projects'
    )
    op.drop_index(
        'idx_projects_view_count',
        table_name='projects'
    )
    op.drop_index(
        'idx_projects_comment_count',
        table_name='projects'
    )
    op.drop_index(
        'idx_votes_user_project',
        table_name='votes'
    )
    op.drop_index(
        'idx_votes_project_vote_type',
        table_name='votes'
    )
