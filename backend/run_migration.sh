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

# Run the migration
echo "Creating initial migration..."
alembic revision --autogenerate -m "Initial migration"

if [ $? -eq 0 ]; then
    echo "✓ Migration created successfully."
else
    echo "✗ Failed to create migration. See error above."
    exit 1
fi

echo ""
echo "Applying migration..."
alembic upgrade head

if [ $? -eq 0 ]; then
    echo "✓ Migration applied successfully."
    echo ""
    echo "Database is now ready!"
    echo "You can start the application with: uvicorn main:app --reload"
else
    echo "✗ Failed to apply migration. See error above."
    exit 1
fi