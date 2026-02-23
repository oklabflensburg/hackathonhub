#!/bin/bash
# Setup Python environment for Hackathon Dashboard backend

echo "Setting up Python environment for Hackathon Dashboard..."

# Check Python version
echo "Checking Python version..."
python3 --version

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
else
    echo "Virtual environment already exists."
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt

# Verify Alembic installation
echo "Verifying Alembic installation..."
if command -v alembic &> /dev/null; then
    echo "✓ Alembic is installed"
    alembic --version
else
    echo "✗ Alembic not found, installing..."
    pip install alembic
fi

# Test database connection
echo ""
echo "Testing database connection..."
python test_db_connection.py

echo ""
echo "Environment setup complete!"
echo ""
echo "To activate the virtual environment manually:"
echo "  cd backend"
echo "  source venv/bin/activate"
echo ""
echo "To run initial migration:"
echo "  alembic revision --autogenerate -m 'Initial migration'"
echo "  alembic upgrade head"
echo ""
echo "To start the application:"
echo "  uvicorn app.main:app --reload"