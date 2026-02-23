"""
Test script to verify the modular structure imports correctly.
"""
import sys
import os

# Add the app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

try:
    # Test core imports
    from app.core.config import settings
    from app.core.database import get_db, SessionLocal
    
    # Test domain imports
    from app.domain.models.base import Base
    from app.domain.models.user import User
    from app.domain.models.project import Project
    from app.domain.schemas.user import UserCreate, User
    
    # Test repository imports
    from app.repositories.base import BaseRepository
    from app.repositories.user_repository import UserRepository
    
    # Test service imports
    from app.services.user_service import UserService, AuthService
    
    # Test API imports
    from app.api.v1.auth.routes import router as auth_router
    
    print("✅ All imports successful!")
    print(f"✅ Config loaded: {settings.APP_NAME}")
    print(f"✅ Models imported: {User.__name__}, {Project.__name__}")
    print(f"✅ Repositories imported: {UserRepository.__name__}")
    print(f"✅ Services imported: {UserService.__name__}, {AuthService.__name__}")
    print(f"✅ API router imported: {auth_router.__name__}")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
except Exception as e:
    print(f"❌ Other error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)