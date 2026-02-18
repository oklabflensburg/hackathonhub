"""Add authentication tables and fields

Revision ID: add_authentication_tables
Revises: 867e99118da7
Create Date: 2026-02-18 13:14:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'add_authentication_tables'
down_revision = '867e99118da7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add columns to users table
    op.add_column('users',
        sa.Column('password_hash', sa.String(), nullable=True))
    op.add_column('users',
        sa.Column('google_id', sa.String(), nullable=True))
    op.add_column('users',
        sa.Column('email_verified', sa.Boolean(),
                  server_default=sa.text('false'), nullable=True))
    op.add_column('users',
        sa.Column('auth_method', sa.String(),
                  server_default=sa.text("'github'"), nullable=True))
    op.add_column('users',
        sa.Column('last_login', sa.DateTime(timezone=True), nullable=True))
    
    # Create refresh_tokens table
    op.create_table('refresh_tokens',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True),
                  server_default=sa.text('now()'), nullable=True),
        sa.Column('revoked_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('replaced_by_token_id', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_refresh_tokens_user_id',
                    'refresh_tokens', ['user_id'], unique=False)
    
    # Create email_verification_tokens table
    op.create_table('email_verification_tokens',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('token', sa.String(), nullable=False),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True),
                  server_default=sa.text('now()'), nullable=True),
        sa.Column('used_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_email_verification_tokens_token',
                    'email_verification_tokens', ['token'], unique=True)
    op.create_index('ix_email_verification_tokens_user_id',
                    'email_verification_tokens', ['user_id'], unique=False)
    
    # Create password_reset_tokens table
    op.create_table('password_reset_tokens',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('token', sa.String(), nullable=False),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True),
                  server_default=sa.text('now()'), nullable=True),
        sa.Column('used_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_password_reset_tokens_token',
                    'password_reset_tokens', ['token'], unique=True)
    op.create_index('ix_password_reset_tokens_user_id',
                    'password_reset_tokens', ['user_id'], unique=False)
    
    # Add unique constraint for google_id
    op.create_index('ix_users_google_id', 'users', ['google_id'], unique=True)


def downgrade() -> None:
    # Drop indexes
    op.drop_index('ix_users_google_id', table_name='users')
    op.drop_index('ix_password_reset_tokens_user_id',
                  table_name='password_reset_tokens')
    op.drop_index('ix_password_reset_tokens_token',
                  table_name='password_reset_tokens')
    op.drop_index('ix_email_verification_tokens_user_id',
                  table_name='email_verification_tokens')
    op.drop_index('ix_email_verification_tokens_token',
                  table_name='email_verification_tokens')
    op.drop_index('ix_refresh_tokens_user_id', table_name='refresh_tokens')
    
    # Drop tables
    op.drop_table('password_reset_tokens')
    op.drop_table('email_verification_tokens')
    op.drop_table('refresh_tokens')
    
    # Drop columns from users table
    op.drop_column('users', 'last_login')
    op.drop_column('users', 'auth_method')
    op.drop_column('users', 'email_verified')
    op.drop_column('users', 'google_id')
    op.drop_column('users', 'password_hash')