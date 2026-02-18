from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# Database URL - using SQLite for development, PostgreSQL for production
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./hackathon.db"
)

# Determine if we're using PostgreSQL and need SSL
is_postgresql = SQLALCHEMY_DATABASE_URL.startswith("postgresql")
connect_args = {}

if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    # SQLite specific connection arguments
    connect_args = {"check_same_thread": False}
elif is_postgresql:
    # PostgreSQL SSL configuration
    # Check if SSL parameters are already in the URL
    if "sslmode=" not in SQLALCHEMY_DATABASE_URL:
        # For production PostgreSQL, we should use SSL
        # Check if we're in production environment
        is_production = os.getenv("ENVIRONMENT", "development") == "production"
        
        if is_production:
            # In production, require SSL by default
            # Append sslmode=require to the connection URL
            if "?" in SQLALCHEMY_DATABASE_URL:
                SQLALCHEMY_DATABASE_URL += "&sslmode=require"
            else:
                SQLALCHEMY_DATABASE_URL += "?sslmode=require"
        
        # For development with local PostgreSQL, we might not need SSL
        # But we can still add sslmode=disable for local development
        # Uncomment to disable SSL for local dev:
        # if not is_production and "localhost" in SQLALCHEMY_DATABASE_URL:
        #     if "?" in SQLALCHEMY_DATABASE_URL:
        #         SQLALCHEMY_DATABASE_URL += "&sslmode=disable"
        #     else:
        #         SQLALCHEMY_DATABASE_URL += "?sslmode=disable"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args=connect_args,
    # Increase connection pool size for production
    pool_size=20,
    max_overflow=30,
    pool_pre_ping=True  # Verify connections before using them
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
