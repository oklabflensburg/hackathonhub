"""Fix refresh_tokens auto-increment issue

Revision ID: fix_refresh_tokens_auto_increment
Revises: add_authentication_tables
Create Date: 2026-02-21 13:28:01.746769

"""
from alembic import op
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision = 'fix_refresh_tokens_auto_increment'
down_revision = 'add_authentication_tables'
branch_labels = None
depends_on = None


def upgrade():
    # Check if we're using PostgreSQL
    bind = op.get_bind()
    if bind.engine.name == 'postgresql':
        # Tables that need auto-increment fixes
        tables_to_fix = [
            'refresh_tokens',
            'email_verification_tokens', 
            'password_reset_tokens'
        ]
        
        for table_name in tables_to_fix:
            # Check if table exists
            table_exists = bind.execute(
                text(f"SELECT EXISTS (SELECT FROM information_schema.tables "
                     f"WHERE table_name = '{table_name}')")
            ).fetchone()[0]
            
            if not table_exists:
                print(f"Table {table_name} doesn't exist, skipping")
                continue
            
            # Check if sequence already exists
            result = bind.execute(
                text(f"SELECT pg_get_serial_sequence('{table_name}', 'id')")
            ).fetchone()
            
            if not result or not result[0]:
                # Get current max id
                max_id_result = bind.execute(
                    text(f"SELECT COALESCE(MAX(id), 0) FROM {table_name}")
                ).fetchone()
                max_id = max_id_result[0] if max_id_result else 0
                next_id = max_id + 1
                
                # Create sequence
                seq_name = f"{table_name}_id_seq"
                sql = f"CREATE SEQUENCE {seq_name} START WITH {next_id}"
                op.execute(sql)
                
                # Set sequence as default for id column
                op.execute(
                    f"ALTER TABLE {table_name} "
                    f"ALTER COLUMN id SET DEFAULT nextval('{seq_name}')"
                )
                
                # Set sequence ownership
                op.execute(
                    f"ALTER SEQUENCE {seq_name} OWNED BY {table_name}.id"
                )
                
                msg = (f"Fixed {table_name} auto-increment: "
                       f"created sequence starting at {next_id}")
                print(msg)
            else:
                print(f"{table_name} already has sequence: {result[0]}")
    else:
        print("Not PostgreSQL, skipping auto-increment fix")


def downgrade():
    # Check if we're using PostgreSQL
    bind = op.get_bind()
    if bind.engine.name == 'postgresql':
        # Tables that might have our sequences
        tables_to_check = [
            'refresh_tokens',
            'email_verification_tokens', 
            'password_reset_tokens'
        ]
        
        for table_name in tables_to_check:
            # Check if table exists
            table_exists = bind.execute(
                text(f"SELECT EXISTS (SELECT FROM information_schema.tables "
                     f"WHERE table_name = '{table_name}')")
            ).fetchone()[0]
            
            if not table_exists:
                print(f"Table {table_name} doesn't exist, skipping")
                continue
            
            # Check if our sequence exists
            result = bind.execute(
                text(f"SELECT pg_get_serial_sequence('{table_name}', 'id')")
            ).fetchone()
            
            seq_name = f"{table_name}_id_seq"
            if result and result[0] == seq_name:
                # Remove default from id column
                op.execute(
                    f"ALTER TABLE {table_name} ALTER COLUMN id DROP DEFAULT"
                )
                
                # Drop the sequence
                op.execute(f"DROP SEQUENCE IF EXISTS {seq_name}")
                
                print(f"Removed {table_name} auto-increment sequence")
            else:
                seq_value = result[0] if result else 'None'
                msg = (f"{table_name}: not our sequence "
                       f"or no sequence: {seq_value}")
                print(msg)
    else:
        print("Not PostgreSQL, skipping auto-increment downgrade")