#!/usr/bin/env python3
"""
Check directory existence and permissions for UPLOAD_DIR.
"""
import os
import sys
import stat
from pathlib import Path

def check_directory(path_str):
    """Check directory existence and permissions."""
    path = Path(path_str)
    
    print(f"Checking directory: {path}")
    print(f"Absolute path: {path.absolute()}")
    
    # Check existence
    if not path.exists():
        print(f"✗ Directory does not exist")
        
        # Check parent directory
        parent = path.parent
        print(f"\nChecking parent directory: {parent}")
        if parent.exists():
            print(f"✓ Parent directory exists")
            # Check if parent is writable
            try:
                test_file = parent / ".test_write"
                test_file.touch()
                test_file.unlink()
                print(f"✓ Parent directory is writable")
                return True, "Directory doesn't exist but parent is writable"
            except Exception as e:
                print(f"✗ Parent directory is not writable: {e}")
                return False, f"Parent directory not writable: {e}"
        else:
            print(f"✗ Parent directory also doesn't exist")
            return False, "Directory and parent don't exist"
    
    # Directory exists
    print(f"✓ Directory exists")
    
    # Check if it's a directory
    if not path.is_dir():
        print(f"✗ Path exists but is not a directory")
        return False, "Path is not a directory"
    
    # Check permissions
    print(f"\nChecking permissions:")
    
    # Get stat info
    st = path.stat()
    
    # Check if readable
    if os.access(str(path), os.R_OK):
        print(f"✓ Readable")
    else:
        print(f"✗ Not readable")
    
    # Check if writable
    if os.access(str(path), os.W_OK):
        print(f"✓ Writable")
    else:
        print(f"✗ Not writable")
        
        # Check ownership
        print(f"\nOwnership check:")
        print(f"  UID: {st.st_uid}, GID: {st.st_gid}")
        print(f"  Current UID: {os.getuid()}, GID: {os.getgid()}")
        
        # Check permissions
        mode = st.st_mode
        print(f"  Permissions: {stat.filemode(mode)}")
        print(f"  Octal: {oct(mode)}")
    
    # Try to create a test file
    try:
        test_file = path / ".test_write"
        test_file.touch()
        test_file.unlink()
        print(f"\n✓ Directory is writable (test file created and deleted)")
        return True, "Directory is writable"
    except Exception as e:
        print(f"\n✗ Directory is not writable: {e}")
        return False, f"Not writable: {e}"

def main():
    # Check the configured UPLOAD_DIR
    upload_dir = "/opt/git/hackathonhub/backend/uploads"
    
    print("=== UPLOAD_DIR Directory Check ===\n")
    
    writable, message = check_directory(upload_dir)
    
    print(f"\n=== Result ===")
    print(f"Directory: {upload_dir}")
    print(f"Writable: {writable}")
    print(f"Message: {message}")
    
    if not writable:
        print(f"\n=== Suggested Fix ===")
        print(f"1. Create directory: sudo mkdir -p {upload_dir}")
        print(f"2. Set permissions: sudo chmod 755 {upload_dir}")
        print(f"3. Set ownership (if needed): sudo chown -R $(whoami):$(whoami) {upload_dir}")
        print(f"4. For web server user: sudo chown -R www-data:www-data {upload_dir}")
    
    return 0 if writable else 1

if __name__ == "__main__":
    sys.exit(main())