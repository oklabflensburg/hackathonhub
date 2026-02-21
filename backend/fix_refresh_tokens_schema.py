#!/usr/bin/env python3
"""
Script to fix the refresh_tokens schema issue where token_id column is missing.
This can be run directly to fix the database without running full migrations.
"""

import sys
import os

# Add parent directory to path before importing database module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import text, inspect
from database import engine, SQLALCHEMY_DATABASE_URL


def fix_refresh_tokens_schema():
    """Check and fix the refresh_tokens table schema"""
    print(f"Database URL: {SQLALCHEMY_DATABASE_URL}")
    print("Checking refresh_tokens table schema...")
    
    # Create a connection
    with engine.connect() as conn:
        # Check if refresh_tokens table exists
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        if 'refresh_tokens' not in tables:
            print("ERROR: refresh_tokens table doesn't exist!")
            print("You need to run the database migrations first.")
            print("Run: cd backend && alembic upgrade head")
            return False
        
        # Check all columns that should exist
        columns = [col['name'] for col in
                   inspector.get_columns('refresh_tokens')]
        print(f"Columns in refresh_tokens table: {columns}")
        
        # Expected columns based on the model
        expected_columns = [
            'id', 'user_id', 'token_id', 'device_info', 'ip_address',
            'user_agent', 'created_at', 'expires_at', 'revoked',
            'revoked_at', 'replaced_by_token_id'
        ]
        
        missing_columns = [
            col for col in expected_columns
            if col not in columns
        ]
        
        if not missing_columns:
            print("✓ All expected columns exist in refresh_tokens table")
            return True
        
        print(f"✗ Missing columns in refresh_tokens table: {missing_columns}")
        print("Attempting to add missing columns...")
        
        try:
            # Determine database type
            dialect = engine.dialect.name
            
            for column in missing_columns:
                print(f"  Adding column: {column}")
                
                if column == 'token_id':
                    if dialect == 'sqlite':
                        conn.execute(text(
                            "ALTER TABLE refresh_tokens "
                            "ADD COLUMN token_id VARCHAR(64)"
                        ))
                        conn.execute(text(
                            "UPDATE refresh_tokens "
                            "SET token_id = 'temp_' || id "
                            "WHERE token_id IS NULL"
                        ))
                    else:  # PostgreSQL
                        conn.execute(text(
                            "ALTER TABLE refresh_tokens "
                            "ADD COLUMN token_id VARCHAR(64)"
                        ))
                        conn.execute(text(
                            "UPDATE refresh_tokens "
                            "SET token_id = 'temp_' || id "
                            "WHERE token_id IS NULL"
                        ))
                        conn.execute(text(
                            "ALTER TABLE refresh_tokens "
                            "ALTER COLUMN token_id SET NOT NULL"
                        ))
                        conn.execute(text(
                            "CREATE UNIQUE INDEX IF NOT EXISTS "
                            "ix_refresh_tokens_token_id "
                            "ON refresh_tokens (token_id)"
                        ))
                
                elif column == 'device_info':
                    if dialect == 'sqlite':
                        conn.execute(text(
                            "ALTER TABLE refresh_tokens "
                            "ADD COLUMN device_info TEXT"
                        ))
                    else:
                        conn.execute(text(
                            "ALTER TABLE refresh_tokens "
                            "ADD COLUMN device_info TEXT"
                        ))
                
                elif column == 'ip_address':
                    if dialect == 'sqlite':
                        conn.execute(text(
                            "ALTER TABLE refresh_tokens "
                            "ADD COLUMN ip_address VARCHAR"
                        ))
                    else:
                        conn.execute(text(
                            "ALTER TABLE refresh_tokens "
                            "ADD COLUMN ip_address VARCHAR"
                        ))
                
                elif column == 'user_agent':
                    if dialect == 'sqlite':
                        conn.execute(text(
                            "ALTER TABLE refresh_tokens "
                            "ADD COLUMN user_agent TEXT"
                        ))
                    else:
                        conn.execute(text(
                            "ALTER TABLE refresh_tokens "
                            "ADD COLUMN user_agent TEXT"
                        ))
                
                elif column == 'created_at':
                    if dialect == 'sqlite':
                        conn.execute(text(
                            "ALTER TABLE refresh_tokens "
                            "ADD COLUMN created_at DATETIME"
                        ))
                    else:
                        conn.execute(text(
                            "ALTER TABLE refresh_tokens "
                            "ADD COLUMN created_at TIMESTAMP WITH TIME ZONE"
                        ))
                
                elif column == 'expires_at':
                    if dialect == 'sqlite':
                        conn.execute(text(
                            "ALTER TABLE refresh_tokens "
                            "ADD COLUMN expires_at DATETIME NOT NULL"
                        ))
                    else:
                        conn.execute(text(
                            "ALTER TABLE refresh_tokens "
                            "ADD COLUMN expires_at TIMESTAMP WITH TIME ZONE "
                            "NOT NULL"
                        ))
                
                elif column == 'revoked':
                    if dialect == 'sqlite':
                        conn.execute(text(
                            "ALTER TABLE refresh_tokens "
                            "ADD COLUMN revoked BOOLEAN DEFAULT 0"
                        ))
                    else:
                        conn.execute(text(
                            "ALTER TABLE refresh_tokens "
                            "ADD COLUMN revoked BOOLEAN DEFAULT FALSE"
                        ))
                
                elif column == 'revoked_at':
                    if dialect == 'sqlite':
                        conn.execute(text(
                            "ALTER TABLE refresh_tokens "
                            "ADD COLUMN revoked_at DATETIME"
                        ))
                    else:
                        conn.execute(text(
                            "ALTER TABLE refresh_tokens "
                            "ADD COLUMN revoked_at TIMESTAMP WITH TIME ZONE"
                        ))
                
                elif column == 'replaced_by_token_id':
                    if dialect == 'sqlite':
                        conn.execute(text(
                            "ALTER TABLE refresh_tokens "
                            "ADD COLUMN replaced_by_token_id VARCHAR(64)"
                        ))
                    else:
                        conn.execute(text(
                            "ALTER TABLE refresh_tokens "
                            "ADD COLUMN replaced_by_token_id VARCHAR(64)"
                        ))
            
            conn.commit()
            print(
                f"✓ Added {len(missing_columns)} missing columns "
                "to refresh_tokens table"
            )
            return True
            
        except Exception as e:
            print(f"ERROR: Failed to add missing columns: {e}")
            import traceback
            traceback.print_exc()
            conn.rollback()
            return False


def check_password_reset_tokens():
    """Check password_reset_tokens table for used column"""
    print("\nChecking password_reset_tokens table...")
    
    with engine.connect():
        inspector = inspect(engine)
        
        if 'password_reset_tokens' not in inspector.get_table_names():
            print("password_reset_tokens table doesn't exist (might be okay)")
            return
        
        columns = [col['name'] for col in
                   inspector.get_columns('password_reset_tokens')]
        print(f"Columns in password_reset_tokens table: {columns}")
        
        if 'used' not in columns:
            print("WARNING: 'used' column missing from password_reset_tokens")
            print("This might cause issues with password reset functionality")


def main():
    """Main function"""
    print("=" * 60)
    print("Database Schema Fix Script")
    print("=" * 60)
    
    try:
        success = fix_refresh_tokens_schema()
        check_password_reset_tokens()
        
        if success:
            print("\n" + "=" * 60)
            print("SUCCESS: Database schema should now be fixed!")
            print("The password reset functionality should work correctly.")
            print("=" * 60)
        else:
            print("\n" + "=" * 60)
            print("FAILED: Could not fix database schema automatically.")
            print("You may need to run database migrations manually:")
            print("  cd backend && alembic upgrade head")
            print("=" * 60)
            sys.exit(1)
            
    except Exception as e:
        print(f"\nERROR: Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()