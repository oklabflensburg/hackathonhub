#!/usr/bin/env python3
"""
Skript zum Hinzufügen der is_persistent Spalte zur refresh_tokens Tabelle.
"""
from app.core.config import settings
from sqlalchemy import create_engine, text
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def main():
    engine = create_engine(settings.DATABASE_URL)

    # Prüfen, ob die Spalte bereits existiert
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT COUNT(*) FROM pragma_table_info('refresh_tokens')
            WHERE name='is_persistent'
        """))
        exists = result.scalar() > 0

        if exists:
            print("Spalte 'is_persistent' existiert bereits.")
            return

        # Spalte hinzufügen
        print("Füge Spalte 'is_persistent' hinzu...")
        conn.execute(text("""
            ALTER TABLE refresh_tokens
            ADD COLUMN is_persistent BOOLEAN DEFAULT FALSE
        """))
        conn.commit()
        print("Spalte erfolgreich hinzugefügt.")


if __name__ == "__main__":
    main()
