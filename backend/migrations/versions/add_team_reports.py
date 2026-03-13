"""add team reports

Revision ID: add_team_reports
Revises: add_team_view_count
Create Date: 2026-03-13 18:05:00.000000
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'add_team_reports'
down_revision: Union[str, None] = 'add_team_view_count'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if not inspector.has_table('team_reports'):
        op.create_table(
            'team_reports',
            sa.Column('id', sa.Integer(), primary_key=True),
            sa.Column('team_id', sa.Integer(), sa.ForeignKey('teams.id'), nullable=False),
            sa.Column('reporter_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
            sa.Column('reason', sa.Text(), nullable=False),
            sa.Column('status', sa.String(length=20), nullable=False, server_default='pending'),
            sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        )

    existing_indexes = {index['name'] for index in inspector.get_indexes('team_reports')}
    if 'ix_team_reports_id' not in existing_indexes:
        op.create_index(op.f('ix_team_reports_id'), 'team_reports', ['id'], unique=False)


def downgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    if inspector.has_table('team_reports'):
        existing_indexes = {index['name'] for index in inspector.get_indexes('team_reports')}
        if 'ix_team_reports_id' in existing_indexes:
            op.drop_index(op.f('ix_team_reports_id'), table_name='team_reports')
        op.drop_table('team_reports')
