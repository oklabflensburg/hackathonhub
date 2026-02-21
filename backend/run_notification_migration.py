#!/usr/bin/env python3
"""Run notification migration directly"""
import sys
from alembic.config import Config
from alembic import command

# Set up Alembic configuration
alembic_cfg = Config("alembic.ini")
alembic_cfg.set_main_option("script_location", "migrations")

print("Running notification migration...")

# Run the migration
try:
    command.upgrade(alembic_cfg, "head")
    print("Migration completed successfully!")
except Exception as e:
    print(f"Migration failed: {e}")
    sys.exit(1)