# Alembic Database Migrations for Hackathon Dashboard

This project now uses Alembic for database migrations with PostgreSQL (installed on the system, not Docker).

## Setup

1. **PostgreSQL Database**: Already created with:
   - Database: `hackathon_db`
   - User: `hackathon_user`
   - Password: `hackathon_password`

2. **Environment Configuration**: The `.env` file is configured to use system PostgreSQL:
   ```
   DATABASE_URL=postgresql://hackathon_user:hackathon_password@localhost:5432/hackathon_db
   ```

## Running Migrations

### Initial Setup (First Time)

1. **Set up Python environment** (if not already done):
   ```bash
   cd backend
   
   # Create and activate virtual environment
   python3 -m venv venv
   source venv/bin/activate
   
   # Install dependencies
   pip install -r requirements.txt
   ```

2. **Run the initial migration** to create all tables:
   ```bash
   alembic revision --autogenerate -m "Initial migration"
   alembic upgrade head
   ```

### Creating New Migrations
When you modify models (in `models.py`), create a new migration:

```bash
cd backend
alembic revision --autogenerate -m "Description of changes"
alembic upgrade head
```

### Common Commands

- **Create migration**: `alembic revision --autogenerate -m "message"`
- **Apply migrations**: `alembic upgrade head`
- **Rollback one migration**: `alembic downgrade -1`
- **Check current revision**: `alembic current`
- **Show migration history**: `alembic history`

## Migration Files

- `alembic.ini` - Alembic configuration
- `migrations/` - Directory containing migration scripts
- `migrations/env.py` - Migration environment
- `migrations/script.py.mako` - Migration template

## Development Workflow

1. Make changes to models in `models.py`
2. Create migration: `alembic revision --autogenerate -m "your message"`
3. Review the generated migration file in `migrations/versions/`
4. Apply migration: `alembic upgrade head`
5. Test your application

## Troubleshooting

### "No changes detected" when creating migration
- Make sure all model imports are included in `migrations/env.py`
- Check that models inherit from `Base` (from `database.py`)

### Connection errors
- Verify PostgreSQL is running: `pg_isready`
- Check credentials in `.env` file
- Ensure database exists: `psql -h localhost -U hackathon_user -d hackathon_db`

### "Multiple head revisions" error
If you see `Multiple head revisions are present for given argument 'head'`:
1. **Option 1: Apply all heads** (recommended):
   ```bash
   alembic upgrade heads
   ```
2. **Option 2: Create a merge migration**:
   ```bash
   # First, check current heads
   alembic heads
   # Then create merge migration (replace with actual revision IDs)
   alembic merge -m "Merge branches" revision1 revision2
   # Apply the merge
   alembic upgrade head
   ```
3. **Option 3: If merge migration already exists** (merge_notification_and_refresh_fixes):
   ```bash
   # Apply both heads first
   alembic upgrade heads
   # Then upgrade to the merge
   alembic upgrade head
   ```

### Reverting to SQLite (for development)
If you want to use SQLite instead:
1. Update `.env`: `DATABASE_URL=sqlite:///./hackathon.db`
2. Uncomment `create_all()` in `main.py`
3. Delete or ignore Alembic files