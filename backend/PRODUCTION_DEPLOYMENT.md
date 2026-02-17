# Production Deployment Guide
## Fixing "attempt to write a readonly database" Error

This guide provides solutions for the SQLite3 operational error occurring during GitHub OAuth user registration.

## Problem
Error: `(sqlite3.OperationalError) attempt to write a readonly database`
Occurs when: Users try to sign in with GitHub OAuth and the application cannot write to the SQLite database.

## Solution Options

### Option 1: Quick Fix (SQLite Permissions) - TEMPORARY
If you need an immediate fix and cannot set up PostgreSQL:

```bash
cd /opt/git/hackathonhub/backend

# Make script executable and run it
chmod +x fix_sqlite_production.sh
./fix_sqlite_production.sh
```

**What this does:**
- Ensures SQLite database file has correct write permissions (666)
- Updates `.env` to use SQLite if not already configured
- Tests database write access

**Limitations:**
- SQLite is not ideal for production web applications
- May have concurrency issues with multiple users
- File permission issues can reoccur

### Option 2: Proper Fix (PostgreSQL with Alembic) - RECOMMENDED
For a production-ready solution:

#### Step 1: Set up PostgreSQL database
```bash
cd /opt/git/hackathonhub/backend

# Run as postgres user or with sudo
chmod +x setup_production_db.sh
sudo ./setup_production_db.sh
```

#### Step 2: Set up Python environment
```bash
cd /opt/git/hackathonhub/backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### Step 3: Run migrations
```bash
# Ensure versions directory exists
mkdir -p migrations/versions

# Create and apply migrations
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

#### Step 4: Start the application
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Option 3: Docker Compose (Alternative)
If you prefer using Docker:

```bash
cd /opt/git/hackathonhub

# Start services
docker-compose up -d db
docker-compose up -d backend
```

## Verification

Test database connection:
```bash
cd /opt/git/hackathonhub/backend
source venv/bin/activate
python test_db_connection.py
```

## Troubleshooting

### "role 'hackathon_user' does not exist"
Run the PostgreSQL setup script: `./setup_production_db.sh`

### "alembic: command not found"
Install dependencies: `pip install -r requirements.txt`

### "No such file or directory: migrations/versions/"
Create the directory: `mkdir -p migrations/versions`

### Still getting "readonly database" error with SQLite
Check file ownership and permissions:
```bash
ls -la hackathon.db
# Should show: -rw-rw-rw-
chmod 666 hackathon.db
chmod 755 .
```

## Configuration Files

### `.env` file for PostgreSQL
```
DATABASE_URL=postgresql://hackathon_user:hackathon_password@localhost:5432/hackathon_db
```

### `.env` file for SQLite (temporary)
```
DATABASE_URL=sqlite:///./hackathon.db
```

## Monitoring

Check application logs:
```bash
# View application logs
journalctl -u hackathonhub.service -f

# Check database connection
sudo -u postgres psql -d hackathon_db -c "SELECT COUNT(*) FROM users;"
```

## Maintenance

### Backup database
```bash
# PostgreSQL backup
sudo -u postgres pg_dump hackathon_db > backup_$(date +%Y%m%d).sql

# SQLite backup
cp hackathon.db hackathon.db.backup
```

### Restore from backup
```bash
# PostgreSQL restore
sudo -u postgres psql hackathon_db < backup_file.sql
```

## Support

For additional help:
1. Check application logs: `journalctl -u hackathonhub.service`
2. Test database connection: `python test_db_connection.py`
3. Verify file permissions: `ls -la hackathon.db`

The recommended solution is **Option 2: PostgreSQL with Alembic** for a production-ready, scalable database setup.