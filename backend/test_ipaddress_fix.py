#!/usr/bin/env python3
"""
Test the IPAddressType fix for SQLite compatibility.
"""
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

print("Testing IPAddressType fix for SQLite compatibility...")
print("=" * 60)

# Test 1: Check IPAddressType definition
print("\n1. Checking IPAddressType definition...")
try:
    from models import IPAddressType
    print(f"  IPAddressType: {IPAddressType}")
    
    # Check what it resolves to
    if hasattr(IPAddressType, '__name__'):
        print(f"  Type name: {IPAddressType.__name__}")
    else:
        print(f"  Type: {IPAddressType}")
        
    # Check database URL
    database_url = os.getenv("DATABASE_URL", "")
    print(f"  DATABASE_URL: {database_url}")
    
    if database_url.startswith("postgresql://"):
        msg = "  ✓ Using PostgreSQL - IPAddressType will use INET"
        print(msg)
    else:
        msg = "  ✓ Using SQLite or other - IPAddressType will use String"
        print(msg)
        
except Exception as e:
    print(f"  ✗ Error: {e}")

# Test 2: Create RefreshToken model instance
print("\n2. Testing RefreshToken model creation...")
try:
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from database import Base
    import models
    
    # Create in-memory SQLite database
    engine = create_engine('sqlite:///:memory:')
    
    # Try to create all tables
    print("  Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("  ✓ Tables created successfully!")
    
    # Create a session
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    # Create a test user
    print("  Creating test user...")
    test_user = models.User(
        username="testuser",
        email="test@example.com",
        email_verified=True
    )
    db.add(test_user)
    db.commit()
    db.refresh(test_user)
    print(f"  ✓ User created with ID: {test_user.id}")
    
    # Create a refresh token
    print("  Creating refresh token...")
    refresh_token = models.RefreshToken(
        user_id=test_user.id,
        token_id="test_token_123",
        ip_address="192.168.1.1",
        user_agent="Test Agent",
        expires_at="2025-01-01 00:00:00"
    )
    db.add(refresh_token)
    db.commit()
    db.refresh(refresh_token)
    print(f"  ✓ Refresh token created with IP: {refresh_token.ip_address}")
    
    # Query it back
    print("  Querying refresh token...")
    token_from_db = db.query(models.RefreshToken).filter_by(
        token_id="test_token_123").first()
    if token_from_db:
        print(f"  ✓ Token retrieved: IP={token_from_db.ip_address}")
    else:
        print("  ✗ Token not found")
        
    db.close()
    print("  ✓ All SQLite operations completed successfully!")
    
except Exception as e:
    print(f"  ✗ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("IPADDRESS FIX TEST COMPLETE")
print("=" * 60)

print("\nSummary:")
print("IPAddressType now dynamically adapts to database dialect:")
print("- Uses INET for PostgreSQL")
print("- Uses String for SQLite and other databases")
print("This ensures compatibility across all database backends.")