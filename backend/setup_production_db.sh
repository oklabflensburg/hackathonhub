#!/bin/bash
# Setup PostgreSQL database for Hackathon Dashboard on production server
# Run this as a user with PostgreSQL admin privileges

echo "Setting up PostgreSQL database for Hackathon Dashboard (Production)"
echo "==================================================================="

# Check if running as postgres or with sudo
if [ "$(whoami)" != "postgres" ]; then
    echo "Note: This script should be run as 'postgres' user or with sudo."
    echo "Trying to run commands with sudo..."
    SUDO_CMD="sudo -u postgres"
else
    SUDO_CMD=""
fi

# Database configuration
DB_NAME="hackathon_db"
DB_USER="hackathon_user"
DB_PASSWORD="hackathon_password"

echo ""
echo "Creating database: $DB_NAME"
$SUDO_CMD psql -c "CREATE DATABASE $DB_NAME;"

echo ""
echo "Creating user: $DB_USER"
$SUDO_CMD psql -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';"

echo ""
echo "Granting privileges..."
$SUDO_CMD psql -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;"

echo ""
echo "Connecting to database to grant schema privileges..."
$SUDO_CMD psql -d $DB_NAME -c "
GRANT ALL ON SCHEMA public TO $DB_USER;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO $DB_USER;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO $DB_USER;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO $DB_USER;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO $DB_USER;
"

echo ""
echo "Verifying setup..."
$SUDO_CMD psql -c "\du $DB_USER"
$SUDO_CMD psql -c "\l $DB_NAME"

echo ""
echo "=========================================="
echo "Database setup complete!"
echo ""
echo "Connection details for .env file:"
echo "DATABASE_URL=postgresql://$DB_USER:$DB_PASSWORD@localhost:5432/$DB_NAME"
echo ""
echo "Next steps:"
echo "1. Update your .env file with the connection string above"
echo "2. Run migrations: cd backend && alembic upgrade head"
echo "3. Start the application: uvicorn main:app --host 0.0.0.0 --port 8000"