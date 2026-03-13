"""add notification enhancements

Revision ID: add_notification_enhancements
Revises: fix_notification_schema
Create Date: 2024-03-13 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision = 'add_notification_enhancements'
down_revision = 'fix_notification_schema'
branch_labels = None
depends_on = None


def upgrade():
    # Add status column to user_notifications
    op.add_column('user_notifications',
                  sa.Column('status', sa.String(50), nullable=True))

    # Add priority column
    op.add_column('user_notifications',
                  sa.Column('priority', sa.String(20),
                            server_default='normal', nullable=True))

    # Add timestamps
    op.add_column('user_notifications',
                  sa.Column('sent_at', sa.DateTime(timezone=True),
                            nullable=True))
    op.add_column('user_notifications',
                  sa.Column('delivered_at', sa.DateTime(timezone=True),
                            nullable=True))
    op.add_column('user_notifications',
                  sa.Column('expires_at', sa.DateTime(timezone=True),
                            nullable=True))

    # Add action URL
    op.add_column('user_notifications',
                  sa.Column('action_url', sa.Text(), nullable=True))

    # Rename channels_sent to channels
    op.alter_column('user_notifications', 'channels_sent',
                    new_column_name='channels')

    # Add platform to push_subscriptions
    op.add_column('push_subscriptions',
                  sa.Column('platform', sa.String(50), nullable=True))
    op.add_column('push_subscriptions',
                  sa.Column('last_used_at', sa.DateTime(timezone=True),
                            nullable=True))

    # Create notification_preferences table
    op.create_table(
        'notification_preferences',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('channels', sa.JSON(), nullable=True),
        sa.Column('notification_types', sa.JSON(), nullable=True),
        sa.Column('quiet_hours', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True),
                  server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True),
                  server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'],
                                ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id')
    )
    op.create_index('ix_notification_preferences_user_id',
                    'notification_preferences', ['user_id'])

    # Update existing records
    op.execute("UPDATE user_notifications SET status = 'sent'")

    bind = op.get_bind()
    channels_type = bind.execute(
        text(
            """
            SELECT data_type
            FROM information_schema.columns
            WHERE table_name = 'user_notifications'
              AND column_name = 'channels'
            """
        )
    ).scalar()

    if channels_type in {"json", "jsonb"}:
        op.execute(
            "UPDATE user_notifications "
            "SET channels = '\"in_app\"'::json "
            "WHERE channels IS NULL"
        )
    else:
        op.execute(
            "UPDATE user_notifications "
            "SET channels = 'in_app' "
            "WHERE channels IS NULL"
        )


def downgrade():
    # Drop notification_preferences table
    op.drop_index('ix_notification_preferences_user_id',
                  table_name='notification_preferences')
    op.drop_table('notification_preferences')

    # Drop columns from push_subscriptions
    op.drop_column('push_subscriptions', 'last_used_at')
    op.drop_column('push_subscriptions', 'platform')

    # Revert channels column name
    op.alter_column('user_notifications', 'channels',
                    new_column_name='channels_sent')

    # Drop columns from user_notifications
    op.drop_column('user_notifications', 'action_url')
    op.drop_column('user_notifications', 'expires_at')
    op.drop_column('user_notifications', 'delivered_at')
    op.drop_column('user_notifications', 'sent_at')
    op.drop_column('user_notifications', 'priority')
    op.drop_column('user_notifications', 'status')
