#!/bin/bash
# Quick fix for SQLite "readonly database" error on production server
# Use this as a temporary solution if PostgreSQL setup is not possible

echo "Fixing SQLite database permissions for Hackathon Dashboard (Production)"
echo "======================================================================="

# Path to SQLite database
DB_FILE="hackathon.db"

echo ""
echo "1. Checking current database configuration..."
if [ -f ".env" ]; then
    DATABASE_URL=$(grep DATABASE_URL .env | cut -d= -f2)
    echo "   Current DATABASE_URL: $DATABASE_URL"
    
    if [[ "$DATABASE_URL" == *"sqlite://"* ]]; then
        echo "   ✓ Already using SQLite"
    else
        echo "   ⚠ Currently using: $(echo $DATABASE_URL | cut -d: -f1)"
        echo "   Switching to SQLite for this fix..."
        # Backup original .env
        cp .env .env.backup
        # Update to SQLite
        sed -i 's|DATABASE_URL=.*|DATABASE_URL=sqlite:///./hackathon.db|' .env
        echo "   Updated .env to use SQLite"
    fi
else
    echo "   ✗ .env file not found"
    exit 1
fi

echo ""
echo "2. Checking SQLite database file..."
if [ -f "$DB_FILE" ]; then
    echo "   ✓ Found $DB_FILE"
    echo "   Current permissions: $(stat -c "%A %U %G" $DB_FILE)"
else
    echo "   ⚠ $DB_FILE not found, creating empty database..."
    touch $DB_FILE
fi

echo ""
echo "3. Fixing permissions..."
# Make sure the file is writable by the web server user
chmod 666 $DB_FILE
echo "   Set permissions to: $(stat -c "%A %U %G" $DB_FILE)"

echo ""
echo "4. Fixing directory permissions..."
chmod 755 .
echo "   Directory permissions updated"

echo ""
echo "5. Testing database write access..."
python3 -c "
import sqlite3
try:
    conn = sqlite3.connect('$DB_FILE')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS test_permissions (id INTEGER PRIMARY KEY)')
    cursor.execute('INSERT INTO test_permissions DEFAULT VALUES')
    conn.commit()
    conn.close()
    print('   ✓ Database is writable')
except Exception as e:
    print(f'   ✗ Database write failed: {e}')
"

echo ""
echo "=========================================="
echo "SQLite fix applied!"
echo ""
echo "Important notes:"
echo "1. This is a TEMPORARY fix for the 'readonly database' error"
echo "2. For production, use PostgreSQL instead of SQLite"
echo "3. To switch back to PostgreSQL:"
echo "   - Restore .env.backup: cp .env.backup .env"
echo "   - Run: ./setup_production_db.sh"
echo "   - Run migrations: alembic upgrade head"
echo ""
echo "The application should now be able to write to the database."