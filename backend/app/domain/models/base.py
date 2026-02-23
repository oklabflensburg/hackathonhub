"""
Base models and custom types for the application.
"""
from sqlalchemy import String
from sqlalchemy.orm import declarative_base
from sqlalchemy import TypeDecorator

# Create declarative base
Base = declarative_base()


class IPAddressType(TypeDecorator):
    """Custom type for IP addresses that adapts to database dialect.
    
    Uses INET for PostgreSQL, String for other databases (SQLite, etc.)
    """
    
    impl = String
    cache_ok = True
    
    def load_dialect_impl(self, dialect):
        # For PostgreSQL, use INET type
        if dialect.name == 'postgresql':
            try:
                from sqlalchemy.dialects.postgresql import INET
                return dialect.type_descriptor(INET)
            except ImportError:
                pass
        # For all other databases (SQLite, MySQL, etc.), use String
        return dialect.type_descriptor(String)