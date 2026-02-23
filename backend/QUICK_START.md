# Quick Start: Fix "readonly database" Error

Follow these steps to fix the "attempt to write a readonly database" error:

## Step 1: Set up Python environment
```bash
cd backend

# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Step 2: Run initial database migration
```bash
# Create and apply initial migration
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

## Step 3: Start the application
```bash
uvicorn app.main:app --reload
```

## Alternative: Use setup script
```bash
cd backend
chmod +x setup_environment.sh
./setup_environment.sh
```

## What was fixed
1. **Database switched from SQLite to PostgreSQL** - eliminates file permission issues
2. **Alembic migrations set up** - proper database version control
3. **Environment configured** - ready for production use

The application should now work without "readonly database" errors when users sign in with GitHub OAuth.