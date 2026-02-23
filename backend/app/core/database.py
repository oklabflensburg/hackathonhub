"""
Database configuration and session management.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
import os

from app.core.config import settings
from app.domain.models.base import Base

# Determine if we're using PostgreSQL and need SSL
is_postgresql = settings.DATABASE_URL.startswith("postgresql")
connect_args = {}

if settings.DATABASE_URL.startswith("sqlite"):
    # SQLite specific connection arguments
    connect_args = {"check_same_thread": False}
elif is_postgresql:
    # PostgreSQL SSL configuration
    # Check if SSL parameters are already in the URL
    if "sslmode=" not in settings.DATABASE_URL:
        # For production PostgreSQL, we should use SSL
        # Check if we're in production environment
        is_production = os.getenv("ENVIRONMENT", "development") == "production"
        
        if is_production:
            # In production, require SSL by default
            # Append sslmode=require to the connection URL
            if "?" in settings.DATABASE_URL:
                settings.DATABASE_URL += "&sslmode=require"
            else:
                settings.DATABASE_URL += "?sslmode=require"
        
        # For development with local PostgreSQL, we might not need SSL
        # But we can still add sslmode=disable for local development
        # Uncomment to disable SSL for local dev:
        # if not is_production and "localhost" in settings.DATABASE_URL:
        #     if "?" in settings.DATABASE_URL:
        #         settings.DATABASE_URL += "&sslmode=disable"
        #     else:
        #         settings.DATABASE_URL += "?sslmode=disable"

# Create database engine
if settings.DATABASE_URL.startswith("sqlite"):
    # SQLite requires special configuration for connection pooling
    engine = create_engine(
        settings.DATABASE_URL,
        connect_args=connect_args,
        poolclass=StaticPool,
        echo=settings.DEBUG
    )
else:
    engine = create_engine(
        settings.DATABASE_URL,
        connect_args=connect_args,
        pool_size=settings.DATABASE_POOL_SIZE,
        max_overflow=settings.DATABASE_MAX_OVERFLOW,
        pool_pre_ping=True,  # Verify connections before using them
        echo=settings.DEBUG
    )

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Session:
    """
    Dependency function to get database session.
    
    Usage:
        @app.get("/items")
        def read_items(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """Create all database tables (for development/testing)."""
    Base.metadata.create_all(bind=engine)


def drop_tables():
    """Drop all database tables (for testing)."""
    Base.metadata.drop_all(bind=engine)