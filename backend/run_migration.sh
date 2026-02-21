#!/bin/bash
# Run Alembic migration for Hackathon Dashboard

echo "Running Alembic migration for Hackathon Dashboard..."
echo ""

# Check if virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Virtual environment not activated. Activating..."
    if [ -d "venv" ]; then
        source venv/bin/activate
        echo "Virtual environment activated."
    else
        echo "Error: Virtual environment not found. Please run setup first."
        echo "Run: python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
        exit 1
    fi
fi

# Check if versions directory exists
if [ ! -d "migrations/versions" ]; then
    echo "Creating migrations/versions directory..."
    mkdir -p migrations/versions
fi

# Check if this is initial setup (no versions directory or empty)
if [ ! -d "migrations/versions" ] || [ -z "$(ls -A migrations/versions 2>/dev/null)" ]; then
    echo "No migrations found. Creating initial migration..."
    alembic revision --autogenerate -m "Initial migration"
    
    if [ $? -eq 0 ]; then
        echo "✓ Migration created successfully."
    else
        echo "✗ Failed to create migration. See error above."
        exit 1
    fi
fi

echo ""
echo "Applying migrations..."
# Use 'heads' instead of 'head' to handle multiple head revisions
alembic upgrade heads

if [ $? -eq 0 ]; then
    echo "✓ Migrations applied successfully."
    echo ""
    echo "Database is now ready!"
    echo "You can start the application with: uvicorn main:app --reload"
else
    echo "✗ Failed to apply migrations. See error above."
    exit 1
fi