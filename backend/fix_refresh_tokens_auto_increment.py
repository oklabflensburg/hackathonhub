#!/usr/bin/env python3
"""
Script to fix the refresh_tokens table auto-increment issue.
The id column needs to have a SERIAL sequence attached to it for PostgreSQL.

This script will:
1. Check if the refresh_tokens table exists
2. Check if the id column already has a sequence
3. If not, create a sequence and set it as the default for the id column
4. Update the sequence to start from the current max id + 1
"""

import sys
import os

# Add parent directory to path before importing database module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import text, inspect
from database import engine, SQLALCHEMY_DATABASE_URL


def fix_refresh_tokens_auto_increment():
    """Fix the auto-increment issue for authentication tables"""
    print(f"Database URL: {SQLALCHEMY_DATABASE_URL}")
    
    if not SQLALCHEMY_DATABASE_URL.startswith("postgresql"):
        print("ERROR: This script is only for PostgreSQL databases.")
        print(f"Current database: {SQLALCHEMY_DATABASE_URL}")
        return False
    
    print("Checking authentication tables auto-increment issues...")
    
    # Tables that need auto-increment fixes
    tables_to_fix = [
        'refresh_tokens',
        'email_verification_tokens',
        'password_reset_tokens'
    ]
    
    # Create a connection
    with engine.connect() as conn:
        all_fixed = True
        
        for table_name in tables_to_fix:
            print(f"\n--- Checking {table_name} ---")
            
            # Check if table exists
            inspector = inspect(engine)
            tables = inspector.get_table_names()
            
            if table_name not in tables:
                print(f"  Table {table_name} doesn't exist, skipping")
                continue
            
            # Check if id column has a sequence
            query = (f"SELECT pg_get_serial_sequence('{table_name}', 'id') "
                     "as seq_name")
            result = conn.execute(text(query))
            seq_row = result.fetchone()
            seq_name = seq_row[0] if seq_row else None
            
            if seq_name:
                print(f"  ✓ Sequence already exists: {seq_name}")
                continue
            
            print(f"  ✗ No sequence found for {table_name}.id column")
            print("  Fixing the auto-increment issue...")
            
            # Start a transaction for this table
            trans = conn.begin()
            try:
                # 1. Get current max id
                query = f"SELECT COALESCE(MAX(id), 0) FROM {table_name}"
                result = conn.execute(text(query))
                max_id = result.fetchone()[0]
                next_id = max_id + 1
                
                print(f"  Current max id: {max_id}, next id: {next_id}")
                
                # 2. Create a sequence for the table
                seq_name = f"{table_name}_id_seq"
                create_seq = f"CREATE SEQUENCE {seq_name} START WITH {next_id}"
                conn.execute(text(create_seq))
                
                # 3. Set the sequence as the default for the id column
                alter_sql = (
                    f"ALTER TABLE {table_name} "
                    f"ALTER COLUMN id SET DEFAULT nextval('{seq_name}')"
                )
                conn.execute(text(alter_sql))
                
                # 4. Set the sequence ownership
                conn.execute(text(
                    f"ALTER SEQUENCE {seq_name} OWNED BY {table_name}.id"
                ))
                
                # Commit the transaction
                trans.commit()
                
                print(f"  ✓ Successfully fixed {table_name} auto-increment!")
                print(f"    - Created sequence: {seq_name}")
                print(f"    - Sequence starts from: {next_id}")
                
            except Exception as e:
                trans.rollback()
                print(f"  ERROR: Failed to fix {table_name}: {e}")
                import traceback
                traceback.print_exc()
                all_fixed = False
        
        if all_fixed:
            print("\n✓ All tables have been checked/fixed successfully!")
            return True
        else:
            print("\n✗ Some tables failed to fix.")
            return False


if __name__ == "__main__":
    success = fix_refresh_tokens_auto_increment()
    sys.exit(0 if success else 1)