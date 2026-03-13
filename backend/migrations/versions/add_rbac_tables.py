"""add rbac tables

Revision ID: add_rbac_tables
Revises: add_team_reports
Create Date: 2026-03-13 20:20:00.000000
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

SYSTEM_ROLE_NAMES = ("user", "moderator", "admin", "superuser")
PERMISSION_CODES = {
    "auth_manage_sessions": "auth:manage_sessions",
    "users_view": "users:view",
    "users_update_self": "users:update_self",
    "users_update_any": "users:update_any",
    "settings_update_self": "settings:update_self",
    "hackathons_create": "hackathons:create",
    "hackathons_update_any": "hackathons:update_any",
    "hackathons_delete_any": "hackathons:delete_any",
    "teams_create": "teams:create",
    "teams_update_any": "teams:update_any",
    "teams_delete_any": "teams:delete_any",
    "team_invitations_create": "team_invitations:create",
    "team_invitations_review": "team_invitations:review",
    "projects_create": "projects:create",
    "projects_update_any": "projects:update_any",
    "projects_delete_any": "projects:delete_any",
    "comments_create": "comments:create",
    "comments_moderate": "comments:moderate",
    "notifications_view_any": "notifications:view_any",
    "notifications_manage": "notifications:manage",
    "uploads_create": "uploads:create",
    "uploads_delete_any": "uploads:delete_any",
    "push_manage_self": "push:manage_self",
    "push_manage_any": "push:manage_any",
    "team_reports_create": "team_reports:create",
    "team_reports_view": "team_reports:view",
    "team_reports_review": "team_reports:review",
    "rbac_view": "rbac:view",
    "rbac_assign_roles": "rbac:assign_roles",
}
ROLE_PERMISSION_MAP = {
    "user": {
        PERMISSION_CODES["users_update_self"],
        PERMISSION_CODES["settings_update_self"],
        PERMISSION_CODES["hackathons_create"],
        PERMISSION_CODES["teams_create"],
        PERMISSION_CODES["projects_create"],
        PERMISSION_CODES["comments_create"],
        PERMISSION_CODES["uploads_create"],
        PERMISSION_CODES["push_manage_self"],
        PERMISSION_CODES["team_reports_create"],
    },
    "moderator": {
        PERMISSION_CODES["users_view"],
        PERMISSION_CODES["comments_moderate"],
        PERMISSION_CODES["notifications_manage"],
        PERMISSION_CODES["notifications_view_any"],
        PERMISSION_CODES["team_reports_view"],
        PERMISSION_CODES["team_reports_review"],
        PERMISSION_CODES["rbac_view"],
    },
    "admin": {
        PERMISSION_CODES["users_view"],
        PERMISSION_CODES["users_update_any"],
        PERMISSION_CODES["hackathons_create"],
        PERMISSION_CODES["hackathons_update_any"],
        PERMISSION_CODES["hackathons_delete_any"],
        PERMISSION_CODES["teams_update_any"],
        PERMISSION_CODES["teams_delete_any"],
        PERMISSION_CODES["team_invitations_create"],
        PERMISSION_CODES["team_invitations_review"],
        PERMISSION_CODES["projects_update_any"],
        PERMISSION_CODES["projects_delete_any"],
        PERMISSION_CODES["comments_moderate"],
        PERMISSION_CODES["notifications_manage"],
        PERMISSION_CODES["notifications_view_any"],
        PERMISSION_CODES["uploads_delete_any"],
        PERMISSION_CODES["push_manage_any"],
        PERMISSION_CODES["team_reports_view"],
        PERMISSION_CODES["team_reports_review"],
        PERMISSION_CODES["rbac_view"],
    },
    "superuser": set(PERMISSION_CODES.values()),
}


revision: str = 'add_rbac_tables'
down_revision: Union[str, None] = 'add_team_reports'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _table_columns(inspector, table_name: str) -> set[str]:
    return {column['name'] for column in inspector.get_columns(table_name)} if inspector.has_table(table_name) else set()


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if not inspector.has_table('roles'):
        op.create_table(
            'roles',
            sa.Column('id', sa.Integer(), primary_key=True),
            sa.Column('name', sa.String(length=50), nullable=False),
            sa.Column('description', sa.String(length=255), nullable=True),
            sa.Column('is_system', sa.Boolean(), nullable=False, server_default=sa.true()),
            sa.Column('created_at', sa.DateTime(timezone=True), nullable=True, server_default=sa.func.now()),
        )
        op.create_index('ix_roles_id', 'roles', ['id'], unique=False)
        op.create_index('ix_roles_name', 'roles', ['name'], unique=True)

    if not inspector.has_table('permissions'):
        op.create_table(
            'permissions',
            sa.Column('id', sa.Integer(), primary_key=True),
            sa.Column('code', sa.String(length=100), nullable=False),
            sa.Column('description', sa.String(length=255), nullable=True),
            sa.Column('resource', sa.String(length=50), nullable=False),
            sa.Column('action', sa.String(length=50), nullable=False),
            sa.Column('created_at', sa.DateTime(timezone=True), nullable=True, server_default=sa.func.now()),
        )
        op.create_index('ix_permissions_id', 'permissions', ['id'], unique=False)
        op.create_index('ix_permissions_code', 'permissions', ['code'], unique=True)

    if not inspector.has_table('role_permissions'):
        op.create_table(
            'role_permissions',
            sa.Column('role_id', sa.Integer(), sa.ForeignKey('roles.id', ondelete='CASCADE'), primary_key=True),
            sa.Column('permission_id', sa.Integer(), sa.ForeignKey('permissions.id', ondelete='CASCADE'), primary_key=True),
            sa.Column('created_at', sa.DateTime(timezone=True), nullable=True, server_default=sa.func.now()),
            sa.UniqueConstraint('role_id', 'permission_id', name='uq_role_permission'),
        )

    if not inspector.has_table('user_roles'):
        op.create_table(
            'user_roles',
            sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True),
            sa.Column('role_id', sa.Integer(), sa.ForeignKey('roles.id', ondelete='CASCADE'), primary_key=True),
            sa.Column('created_at', sa.DateTime(timezone=True), nullable=True, server_default=sa.func.now()),
            sa.UniqueConstraint('user_id', 'role_id', name='uq_user_role'),
        )

    inspector = sa.inspect(bind)
    report_columns = _table_columns(inspector, 'team_reports')
    if 'reviewed_by' not in report_columns:
        op.add_column('team_reports', sa.Column('reviewed_by', sa.Integer(), sa.ForeignKey('users.id'), nullable=True))
    if 'reviewed_at' not in report_columns:
        op.add_column('team_reports', sa.Column('reviewed_at', sa.DateTime(timezone=True), nullable=True))
    if 'resolution_note' not in report_columns:
        op.add_column('team_reports', sa.Column('resolution_note', sa.Text(), nullable=True))

    role_table = sa.table(
        'roles',
        sa.column('id', sa.Integer()),
        sa.column('name', sa.String()),
        sa.column('description', sa.String()),
        sa.column('is_system', sa.Boolean()),
    )
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
    user_role_table = sa.table(
        'user_roles',
        sa.column('user_id', sa.Integer()),
        sa.column('role_id', sa.Integer()),
    )

    role_rows = bind.execute(sa.text('SELECT id, name FROM roles')).fetchall()
    existing_roles = {row.name: row.id for row in role_rows}
    roles_to_insert = [
        {'name': role_name, 'description': f'System role: {role_name}', 'is_system': True}
        for role_name in SYSTEM_ROLE_NAMES
        if role_name not in existing_roles
    ]
    if roles_to_insert:
        op.bulk_insert(role_table, roles_to_insert)
        role_rows = bind.execute(sa.text('SELECT id, name FROM roles')).fetchall()
        existing_roles = {row.name: row.id for row in role_rows}

    permission_rows = bind.execute(sa.text('SELECT id, code FROM permissions')).fetchall()
    existing_permissions = {row.code: row.id for row in permission_rows}
    permission_inserts = []
    for code in PERMISSION_CODES.values():
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

    existing_role_permissions = {
        (row.role_id, row.permission_id)
        for row in bind.execute(sa.text('SELECT role_id, permission_id FROM role_permissions')).fetchall()
    }
    role_permission_inserts = []
    for role_name, permission_codes in ROLE_PERMISSION_MAP.items():
        role_id = existing_roles[role_name]
        for code in permission_codes:
            permission_id = existing_permissions[code]
            if (role_id, permission_id) not in existing_role_permissions:
                role_permission_inserts.append({'role_id': role_id, 'permission_id': permission_id})
    if role_permission_inserts:
        op.bulk_insert(role_permission_table, role_permission_inserts)

    default_role_id = existing_roles['user']
    existing_user_role_user_ids = {row.user_id for row in bind.execute(sa.text('SELECT user_id FROM user_roles')).fetchall()}
    user_rows = bind.execute(sa.text('SELECT id FROM users')).fetchall()
    user_role_inserts = [{'user_id': row.id, 'role_id': default_role_id} for row in user_rows if row.id not in existing_user_role_user_ids]
    if user_role_inserts:
        op.bulk_insert(user_role_table, user_role_inserts)


def downgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    report_columns = _table_columns(inspector, 'team_reports')
    if 'resolution_note' in report_columns:
        op.drop_column('team_reports', 'resolution_note')
    if 'reviewed_at' in report_columns:
        op.drop_column('team_reports', 'reviewed_at')
    if 'reviewed_by' in report_columns:
        op.drop_column('team_reports', 'reviewed_by')

    if inspector.has_table('user_roles'):
        op.drop_table('user_roles')
    if inspector.has_table('role_permissions'):
        op.drop_table('role_permissions')
    if inspector.has_table('permissions'):
        existing_indexes = {index['name'] for index in inspector.get_indexes('permissions')}
        if 'ix_permissions_code' in existing_indexes:
            op.drop_index('ix_permissions_code', table_name='permissions')
        if 'ix_permissions_id' in existing_indexes:
            op.drop_index('ix_permissions_id', table_name='permissions')
        op.drop_table('permissions')
    if inspector.has_table('roles'):
        existing_indexes = {index['name'] for index in inspector.get_indexes('roles')}
        if 'ix_roles_name' in existing_indexes:
            op.drop_index('ix_roles_name', table_name='roles')
        if 'ix_roles_id' in existing_indexes:
            op.drop_index('ix_roles_id', table_name='roles')
        op.drop_table('roles')
