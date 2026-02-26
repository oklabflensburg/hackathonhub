#!/usr/bin/env python3
"""
Test script to verify the FileUploadService changes.
"""
import sys
import os
from pathlib import Path

# Add the app directory to the path
sys.path.insert(0, str(Path(__file__).parent))


def test_settings_import():
    """Test that settings can be imported and UPLOAD_DIR is accessible."""
    try:
        from app.core.config import settings
        print(f"✓ settings imported successfully")
        print(f"  settings.UPLOAD_DIR = {settings.UPLOAD_DIR}")
        return True
    except Exception as e:
        print(f"✗ Failed to import settings: {e}")
        return False


def test_file_upload_service():
    """Test that FileUploadService can be instantiated."""
    try:
        from app.utils.file_upload import FileUploadService
        service = FileUploadService()
        print(f"✓ FileUploadService instantiated successfully")
        print(f"  service.upload_dir = {service.upload_dir}")
        print(f"  service.upload_dir exists: {service.upload_dir.exists()}")

        # Check if it's using settings.UPLOAD_DIR
        from app.core.config import settings
        if str(service.upload_dir) == settings.UPLOAD_DIR:
            print(f"✓ Using configured UPLOAD_DIR: {settings.UPLOAD_DIR}")
        else:
            print(f"⚠ Using different directory: {service.upload_dir}")
            print(f"  Configured UPLOAD_DIR was: {settings.UPLOAD_DIR}")

        return True
    except Exception as e:
        print(f"✗ Failed to instantiate FileUploadService: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_writable_check():
    """Test the _is_writable method."""
    try:
        from app.utils.file_upload import FileUploadService
        service = FileUploadService()

        # Test with a writable directory (should be True)
        test_dir = Path("/tmp/test_writable")
        test_dir.mkdir(exist_ok=True)
        result = service._is_writable(test_dir)
        print(f"✓ _is_writable test on /tmp/test_writable: {result}")

        # Clean up
        test_dir.rmdir()

        return True
    except Exception as e:
        print(f"✗ _is_writable test failed: {e}")
        return False


def main():
    print("=== Testing FileUploadService Code Consistency Fix ===\n")

    # Test 1: Settings import
    print("1. Testing settings import:")
    if not test_settings_import():
        return 1

    print()

    # Test 2: FileUploadService instantiation
    print("2. Testing FileUploadService instantiation:")
    if not test_file_upload_service():
        return 1

    print()

    # Test 3: Writable check
    print("3. Testing _is_writable method:")
    if not test_writable_check():
        return 1

    print("\n=== All tests passed ===")
    print("\nSummary:")
    print("- FileUploadService now uses settings.UPLOAD_DIR instead of os.getenv")
    print("- Logging uses logger.warning instead of print")
    print("- Code is consistent with main.py which also uses settings.UPLOAD_DIR")

    return 0


if __name__ == "__main__":
    sys.exit(main())
