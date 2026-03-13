"""add generic reports

Revision ID: add_generic_reports
Revises: add_rbac_tables
Create Date: 2026-03-13 22:30:00.000000
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = 'add_generic_reports'
down_revision: Union[str, None] = 'add_rbac_tables'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

NEW_PERMISSION_CODES = {
    'reports_create': 'reports:create',
    'reports_view': 'reports:view',
    'reports_review': 'reports:review',
}

ROLE_PERMISSION_MAP = {
    'user': {'reports:create'},
    'moderator': {'reports:view', 'reports:review'},
    'admin': {'reports:view', 'reports:review'},
    'superuser': {'reports:create', 'reports:view', 'reports:review'},
}


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if not inspector.has_table('reports'):
        op.create_table(
            'reports',
            sa.Column('id', sa.Integer(), primary_key=True),
            sa.Column('reporter_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
            sa.Column('resource_type', sa.String(length=20), nullable=False),
            sa.Column('resource_id', sa.Integer(), nullable=False),
            sa.Column('reason', sa.Text(), nullable=False),
            sa.Column('status', sa.String(length=20), nullable=False, server_default='pending'),
            sa.Column('resolution_note', sa.Text(), nullable=True),
            sa.Column('reviewed_by', sa.Integer(), sa.ForeignKey('users.id'), nullable=True),
            sa.Column('reviewed_at', sa.DateTime(timezone=True), nullable=True),
            sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        )
        op.create_index('ix_reports_resource', 'reports', ['resource_type', 'resource_id'], unique=False)
        op.create_index('ix_reports_status', 'reports', ['status'], unique=False)
        op.create_index('ix_reports_reporter_id', 'reports', ['reporter_id'], unique=False)
        op.create_index('ix_reports_reviewed_by', 'reports', ['reviewed_by'], unique=False)
        op.create_index('ix_reports_created_at', 'reports', ['created_at'], unique=False)

    permission_table = sa.table(
        'permissions',
        sa.column('id', sa.Integer()),
        sa.column('code', sa.String()),
        sa.column('description', sa.String()),
        sa.column('resource', sa.String()),
        sa.column('action', sa.String()),
    )
    role_permission_table = sa.table(
        'role_permissions',
        sa.column('role_id', sa.Integer()),
        sa.column('permission_id', sa.Integer()),
    )

    permission_rows = bind.execute(sa.text('SELECT id, code FROM permissions')).fetchall()
    existing_permissions = {row.code: row.id for row in permission_rows}
    permission_inserts = []
    for code in NEW_PERMISSION_CODES.values():
        if code in existing_permissions:
            continue
        resource, action = code.split(':', 1)
        permission_inserts.append({
            'code': code,
            'description': code.replace(':', ' '),
            'resource': resource,
            'action': action,
        })
    if permission_inserts:
        op.bulk_insert(permission_table, permission_inserts)
        permission_rows = bind.execute(sa.text('SELECT id, code FROM permissions')).fetchall()
        existing_permissions = {row.code: row.id for row in permission_rows}

    roles = {row.name: row.id for row in bind.execute(sa.text('SELECT id, name FROM roles')).fetchall()}
    existing_role_permissions = {(row.role_id, row.permission_id) for row in bind.execute(sa.text('SELECT role_id, permission_id FROM role_permissions')).fetchall()}
    inserts = []
    for role_name, codes in ROLE_PERMISSION_MAP.items():
        role_id = roles.get(role_name)
        if not role_id:
            continue
        for code in codes:
            permission_id = existing_permissions.get(code)
            if permission_id and (role_id, permission_id) not in existing_role_permissions:
                inserts.append({'role_id': role_id, 'permission_id': permission_id})
    if inserts:
        op.bulk_insert(role_permission_table, inserts)


def downgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if inspector.has_table('reports'):
        existing_indexes = {index['name'] for index in inspector.get_indexes('reports')}
        for index_name in ('ix_reports_resource', 'ix_reports_status', 'ix_reports_reporter_id', 'ix_reports_reviewed_by', 'ix_reports_created_at'):
            if index_name in existing_indexes:
                op.drop_index(index_name, table_name='reports')
        op.drop_table('reports')

    codes = tuple(NEW_PERMISSION_CODES.values())
    if codes:
        bind.execute(sa.text('DELETE FROM role_permissions WHERE permission_id IN (SELECT id FROM permissions WHERE code IN :codes)').bindparams(sa.bindparam('codes', expanding=True)), {'codes': list(codes)})
        bind.execute(sa.text('DELETE FROM permissions WHERE code IN :codes').bindparams(sa.bindparam('codes', expanding=True)), {'codes': list(codes)})
