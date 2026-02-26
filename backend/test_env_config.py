#!/usr/bin/env python3
"""
Test if the .env configuration is loaded correctly.
"""
import sys
import os
from pathlib import Path

# Add the app directory to the path
sys.path.insert(0, str(Path(__file__).parent))

def test_env_loading():
    """Test that UPLOAD_DIR is loaded from .env"""
    print("=== Testing .env Configuration Loading ===\n")
    
    # First, check if pydantic_settings is available
    try:
        from pydantic_settings import BaseSettings
        print("✓ pydantic_settings is available")
    except ImportError as e:
        print(f"✗ pydantic_settings not available: {e}")
        print("  This is expected in test environment")
        return False
    
    # Try to load settings
    try:
        from app.core.config import Settings, settings
        
        print(f"✓ Settings class loaded")
        print(f"✓ settings instance created")
        
        # Check UPLOAD_DIR value
        print(f"\nConfiguration values:")
        print(f"  settings.UPLOAD_DIR = {settings.UPLOAD_DIR}")
        print(f"  settings.APP_NAME = {settings.APP_NAME}")
        print(f"  settings.DEBUG = {settings.DEBUG}")
        
        # Check if UPLOAD_DIR is the expected value
        expected_upload_dir = "./uploads"
        if settings.UPLOAD_DIR == expected_upload_dir:
            print(f"\n✓ UPLOAD_DIR is correctly set to '{expected_upload_dir}'")
            
            # Check if the directory exists and is writable
            upload_path = Path(settings.UPLOAD_DIR)
            if not upload_path.is_absolute():
                # Make it absolute relative to backend directory
                upload_path = Path(__file__).parent / settings.UPLOAD_DIR
            
            print(f"\nChecking directory: {upload_path}")
            print(f"  Exists: {upload_path.exists()}")
            
            if upload_path.exists():
                # Check if writable
                try:
                    test_file = upload_path / ".test_write"
                    test_file.touch()
                    test_file.unlink()
                    print(f"  Writable: YES")
                    print(f"\n✓ Directory is accessible and writable")
                    return True
                except Exception as e:
                    print(f"  Writable: NO - {e}")
                    print(f"\n⚠ Directory exists but is not writable")
                    return False
            else:
                print(f"\n⚠ Directory does not exist (but might be created at runtime)")
                return True
        else:
            print(f"\n✗ UPLOAD_DIR is '{settings.UPLOAD_DIR}', expected '{expected_upload_dir}'")
            return False
            
    except Exception as e:
        print(f"✗ Failed to load settings: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    success = test_env_loading()
    
    print(f"\n=== Test {'PASSED' if success else 'FAILED'} ===")
    
    if success:
        print("\nNext steps:")
        print("1. Restart the application to load the new .env configuration")
        print("2. Check logs for 'Using fallback upload directory' warnings")
        print("3. Test file upload functionality")
    else:
        print("\nTroubleshooting:")
        print("1. Check that pydantic_settings is installed: pip install pydantic-settings")
        print("2. Verify .env file is in the correct location")
        print("3. Check file permissions on .env file")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())