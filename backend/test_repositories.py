#!/usr/bin/env python3
"""
Test script to verify repository functionality.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.database import Base
from app.repositories.refresh_token_repository import RefreshTokenRepository
from app.repositories.password_reset_token_repository import PasswordResetTokenRepository
from app.repositories.vote_repository import VoteRepository
from app.repositories.file_repository import FileRepository
from datetime import datetime, timedelta

# Create in-memory SQLite database for testing
engine = create_engine('sqlite:///:memory:')
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def test_repository_creation():
    """Test that repositories can be instantiated."""
    print("Testing repository creation...")
    
    try:
        refresh_repo = RefreshTokenRepository()
        password_repo = PasswordResetTokenRepository()
        vote_repo = VoteRepository()
        file_repo = FileRepository()
        
        print("✅ All repositories created successfully")
        return True
    except Exception as e:
        print(f"❌ Error creating repositories: {e}")
        return False

def test_repository_methods():
    """Test basic repository methods."""
    print("\nTesting repository methods...")
    
    db = SessionLocal()
    
    try:
        # Test RefreshTokenRepository
        refresh_repo = RefreshTokenRepository()
        
        # Test create_with_details
        token = refresh_repo.create_with_details(
            db=db,
            user_id=1,
            token_id="test_token_123",
            expires_at=datetime.utcnow() + timedelta(days=7)
        )
        print(f"✅ RefreshToken created: {token.token_id}")
        
        # Test get_by_token_id
        retrieved = refresh_repo.get_by_token_id(db, "test_token_123")
        print(f"✅ RefreshToken retrieved: {retrieved.token_id if retrieved else 'None'}")
        
        # Test PasswordResetTokenRepository
        password_repo = PasswordResetTokenRepository()
        
        # Test create_token
        reset_token = password_repo.create_token(
            db=db,
            user_id=1,
            token="reset_token_456",
            expires_at=datetime.utcnow() + timedelta(hours=1)
        )
        print(f"✅ PasswordResetToken created: {reset_token.token}")
        
        # Test get_by_token
        retrieved_reset = password_repo.get_by_token(db, "reset_token_456")
        print(f"✅ PasswordResetToken retrieved: {retrieved_reset.token if retrieved_reset else 'None'}")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ Error testing repository methods: {e}")
        db.close()
        return False

def main():
    """Run all tests."""
    print("=" * 60)
    print("Repository Functionality Test")
    print("=" * 60)
    
    success = True
    
    # Test 1: Repository creation
    if not test_repository_creation():
        success = False
    
    # Test 2: Repository methods
    if not test_repository_methods():
        success = False
    
    print("\n" + "=" * 60)
    if success:
        print("✅ All repository tests passed!")
    else:
        print("❌ Some repository tests failed")
    print("=" * 60)
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())