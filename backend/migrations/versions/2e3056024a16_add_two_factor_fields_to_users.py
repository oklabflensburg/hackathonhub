"""add_two_factor_fields_to_users

Revision ID: 2e3056024a16
Revises: add_project_performance_indexes
Create Date: 2026-03-09 17:19:55.660395

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2e3056024a16'
down_revision = 'add_project_performance_indexes'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add two-factor authentication fields to users table
    op.add_column('users',
                  sa.Column('two_factor_secret', sa.String(), nullable=True))
    op.add_column('users',
                  sa.Column('two_factor_backup_codes', sa.String(),
                            nullable=True))
    op.add_column('users',
                  sa.Column('two_factor_enabled', sa.Boolean(),
                            server_default='false', nullable=False))


def downgrade() -> None:
    # Remove two-factor authentication fields
    op.drop_column('users', 'two_factor_enabled')
    op.drop_column('users', 'two_factor_backup_codes')
    op.drop_column('users', 'two_factor_secret')
