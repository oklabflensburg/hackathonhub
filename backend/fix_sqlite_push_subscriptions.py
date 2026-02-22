#!/usr/bin/env python3
"""
Simple script to fix push_subscriptions.user_agent column for SQLite (hackathon.db).
"""
import sqlite3
import os

def main():
    db_path = 'hackathon.db'
    
    if not os.path.exists(db_path):
        print(f"Error: Database file '{db_path}' not found.")
        print("Make sure you're in the backend directory or provide the correct path.")
        return
    
    print(f"Opening SQLite database: {db_path}")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if user_agent column exists
        cursor.execute("PRAGMA table_info(push_subscriptions)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'user_agent' in columns:
            print("✓ user_agent column already exists in push_subscriptions table")
        else:
            print("Adding user_agent column to push_subscriptions table...")
            cursor.execute("ALTER TABLE push_subscriptions ADD COLUMN user_agent TEXT")
            print("✓ Column added successfully")
        
        # Update alembic_version table
        cursor.execute("SELECT version_num FROM alembic_version")
        current_version = cursor.fetchone()
        if current_version:
            current_version = current_version[0]
            print(f"Current alembic version: {current_version}")
            
            # Update to our migration ID
            cursor.execute("UPDATE alembic_version SET version_num = 'add_user_agent_to_push'")
            print("✓ Alembic version updated to 'add_user_agent_to_push'")
        else:
            print("Warning: alembic_version table not found or empty")
        
        conn.commit()
        conn.close()
        
        print("\n✅ Fix applied successfully!")
        print("The /api/push-subscriptions endpoint should now work correctly.")
        
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()