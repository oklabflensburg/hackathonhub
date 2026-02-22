#!/usr/bin/env python3
"""
Script to fix the push_subscriptions.user_agent column issue.
This can be run instead of the Alembic migration if there are issues.
"""
import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.exc import ProgrammingError

def get_db_url():
    """Get database URL from environment or use default."""
    db_url = os.getenv('DATABASE_URL')
    if not db_url:
        # Check if using SQLite (hackathon.db)
        if os.path.exists('hackathon.db'):
            db_url = 'sqlite:///hackathon.db'
        else:
            # Default local PostgreSQL
            db_url = 'postgresql://postgres:postgres@localhost:5432/hackathon_dashboard'
    return db_url

def check_column_exists(engine, table_name, column_name):
    """Check if a column exists in a table."""
    with engine.connect() as conn:
        result = conn.execute(text(f"""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = '{table_name}' 
            AND column_name = '{column_name}'
        """))
        return result.fetchone() is not None

def add_user_agent_column(engine):
    """Add user_agent column to push_subscriptions table."""
    with engine.connect() as conn:
        print("Checking if user_agent column exists...")
        if check_column_exists(engine, 'push_subscriptions', 'user_agent'):
            print("✓ user_agent column already exists")
            return True
        
        print("Adding user_agent column to push_subscriptions table...")
        try:
            conn.execute(text("ALTER TABLE push_subscriptions ADD COLUMN user_agent TEXT"))
            conn.commit()
            print("✓ Column added successfully")
            return True
        except Exception as e:
            print(f"✗ Error adding column: {e}")
            return False

def update_alembic_version(engine):
    """Update alembic_version table to mark migration as applied."""
    with engine.connect() as conn:
        print("Updating alembic_version table...")
        try:
            # Check current version
            result = conn.execute(text("SELECT version_num FROM alembic_version"))
            current_version = result.fetchone()[0]
            print(f"Current alembic version: {current_version}")
            
            # Update to our migration ID
            conn.execute(text(
                "UPDATE alembic_version SET version_num = 'add_user_agent_to_push'"
            ))
            conn.commit()
            print("✓ Alembic version updated to 'add_user_agent_to_push'")
            return True
        except Exception as e:
            print(f"✗ Error updating alembic_version: {e}")
            return False

def main():
    """Main function."""
    print("Fixing push_subscriptions.user_agent column issue...")
    
    db_url = get_db_url()
    print(f"Connecting to database: {db_url.split('@')[-1] if '@' in db_url else db_url}")
    
    try:
        engine = create_engine(db_url)
        
        # Test connection
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        
        print("✓ Database connection successful")
        
        # Add the column
        if not add_user_agent_column(engine):
            sys.exit(1)
        
        # Update alembic version
        update_alembic_version(engine)
        
        print("\n✅ Fix applied successfully!")
        print("The /api/push-subscriptions endpoint should now work correctly.")
        
    except Exception as e:
        print(f"✗ Database error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()