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
        
        # Check if token_id column exists
        columns = [col['name'] for col in
                   inspector.get_columns('refresh_tokens')]
        print(f"Columns in refresh_tokens table: {columns}")
        
        if 'token_id' in columns:
            print("✓ token_id column already exists in refresh_tokens table")
            return True
        
        print("✗ token_id column is missing from refresh_tokens table")
        print("Attempting to add token_id column...")
        
        try:
            # Determine database type
            dialect = engine.dialect.name
            
            if dialect == 'sqlite':
                # SQLite: add column
                conn.execute(text(
                    "ALTER TABLE refresh_tokens "
                    "ADD COLUMN token_id VARCHAR(64)"
                ))
                # Set temporary values
                conn.execute(text(
                    "UPDATE refresh_tokens SET token_id = 'temp_' || id "
                    "WHERE token_id IS NULL"
                ))
                # Create index
                conn.execute(text(
                    "CREATE UNIQUE INDEX ix_refresh_tokens_token_id "
                    "ON refresh_tokens (token_id)"
                ))
                conn.commit()
                print("✓ Added token_id column to refresh_tokens (SQLite)")
                
            elif dialect in ('postgresql', 'postgres'):
                # PostgreSQL: add column
                conn.execute(text(
                    "ALTER TABLE refresh_tokens "
                    "ADD COLUMN token_id VARCHAR(64)"
                ))
                # Set temporary values
                conn.execute(text(
                    "UPDATE refresh_tokens SET token_id = 'temp_' || id "
                    "WHERE token_id IS NULL"
                ))
                # Make column NOT NULL
                conn.execute(text(
                    "ALTER TABLE refresh_tokens "
                    "ALTER COLUMN token_id SET NOT NULL"
                ))
                # Create index
                conn.execute(text(
                    "CREATE UNIQUE INDEX ix_refresh_tokens_token_id "
                    "ON refresh_tokens (token_id)"
                ))
                conn.commit()
                print("✓ Added token_id column to refresh_tokens (PostgreSQL)")
                
            else:
                print(f"ERROR: Unsupported database dialect: {dialect}")
                return False
                
            return True
            
        except Exception as e:
            print(f"ERROR: Failed to add token_id column: {e}")
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