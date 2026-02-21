"""Add notification tables

Revision ID: add_notification_tables
Revises: add_team_id_to_projects
Create Date: 2026-02-21 12:40:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'add_notification_tables'
down_revision = 'add_team_id_to_projects'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create notification_types table
    op.create_table(
        'notification_types',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('default_email', sa.Boolean(),
                  server_default=sa.text('true'), nullable=False),
        sa.Column('default_push', sa.Boolean(),
                  server_default=sa.text('true'), nullable=False),
        sa.Column('default_in_app', sa.Boolean(),
                  server_default=sa.text('true'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True),
                  server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )

    # Create user_notification_preferences table
    op.create_table(
        'user_notification_preferences',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('notification_type_id', sa.Integer(), nullable=False),
        sa.Column('email_enabled', sa.Boolean(),
                  server_default=sa.text('true'), nullable=False),
        sa.Column('push_enabled', sa.Boolean(),
                  server_default=sa.text('true'), nullable=False),
        sa.Column('in_app_enabled', sa.Boolean(),
                  server_default=sa.text('true'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True),
                  server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True),
                  server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['notification_type_id'], [
                                'notification_types.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id', 'notification_type_id',
                            name='uq_user_notification_type')
    )

    # Create user_notifications table
    op.create_table(
        'user_notifications',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('notification_type', sa.String(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('message', sa.String(), nullable=False),
        sa.Column('data', postgresql.JSONB(), nullable=True),
        sa.Column('channels_sent', postgresql.JSONB(), nullable=True),
        sa.Column('read_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True),
                  server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create push_subscriptions table
    op.create_table(
        'push_subscriptions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('endpoint', sa.String(), nullable=False),
        sa.Column('p256dh', sa.String(), nullable=False),
        sa.Column('auth', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True),
                  server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True),
                  server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('endpoint')
    )

    # Create index for faster queries
    op.create_index('ix_user_notifications_user_id',
                    'user_notifications', ['user_id'])
    op.create_index('ix_user_notifications_created_at',
                    'user_notifications', ['created_at'])
    op.create_index('ix_user_notifications_read_at',
                    'user_notifications', ['read_at'])
    op.create_index('ix_user_notification_preferences_user_id',
                    'user_notification_preferences', ['user_id'])
    op.create_index('ix_push_subscriptions_user_id',
                    'push_subscriptions', ['user_id'])


def downgrade() -> None:
    # Drop indexes
    op.drop_index('ix_push_subscriptions_user_id')
    op.drop_index('ix_user_notification_preferences_user_id')
    op.drop_index('ix_user_notifications_read_at')
    op.drop_index('ix_user_notifications_created_at')
    op.drop_index('ix_user_notifications_user_id')

    # Drop tables in reverse order
    op.drop_table('push_subscriptions')
    op.drop_table('user_notifications')
    op.drop_table('user_notification_preferences')
    op.drop_table('notification_types')
