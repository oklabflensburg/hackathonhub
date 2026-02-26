#!/usr/bin/env python3
"""
Test script to check UPLOAD_DIR environment and permissions.
"""
import os
import sys
from pathlib import Path

def check_upload_dir():
    print("=== UPLOAD_DIR Environment Check ===")
    
    # Check environment variable
    upload_dir_env = os.getenv("UPLOAD_DIR")
    print(f"1. os.getenv('UPLOAD_DIR'): {upload_dir_env}")
    
    # Check settings from config
    try:
        from app.core.config import settings
        print(f"2. settings.UPLOAD_DIR: {settings.UPLOAD_DIR}")
    except Exception as e:
        print(f"2. Failed to import settings: {e}")
    
    # Check default from file_upload.py logic
    default_dir = "./uploads"
    upload_dir = os.getenv("UPLOAD_DIR", default_dir)
    print(f"3. Combined (os.getenv with default): {upload_dir}")
    
    # Check if directory exists and is writable
    upload_path = Path(upload_dir)
    print(f"4. Path: {upload_path.absolute()}")
    print(f"5. Exists: {upload_path.exists()}")
    print(f"6. Is directory: {upload_path.is_dir() if upload_path.exists() else 'N/A'}")
    
    # Check writable
    def is_writable(path):
        try:
            test_file = path / ".write_test"
            test_file.touch()
            test_file.unlink()
            return True
        except (OSError, IOError) as e:
            return False, str(e)
    
    if upload_path.exists():
        writable, error = is_writable(upload_path)
        print(f"7. Writable: {writable}")
        if not writable:
            print(f"   Error: {error}")
    else:
        print(f"7. Directory does not exist, checking parent...")
        parent = upload_path.parent
        print(f"   Parent: {parent.absolute()}")
        print(f"   Parent exists: {parent.exists()}")
        if parent.exists():
            writable, error = is_writable(parent)
            print(f"   Parent writable: {writable}")
            if not writable:
                print(f"   Parent error: {error}")
    
    # Check /tmp/uploads
    tmp_upload = Path("/tmp/uploads")
    print(f"\n8. /tmp/uploads check:")
    print(f"   Path: {tmp_upload.absolute()}")
    print(f"   Exists: {tmp_upload.exists()}")
    if tmp_upload.exists():
        writable, error = is_writable(tmp_upload)
        print(f"   Writable: {writable}")
        if not writable:
            print(f"   Error: {error}")
    
    # Check current working directory
    print(f"\n9. Current working directory: {Path.cwd()}")
    print(f"10. Backend directory: {Path(__file__).parent.absolute()}")

if __name__ == "__main__":
