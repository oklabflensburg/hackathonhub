#!/usr/bin/env python3
import json
import sys

def validate_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"✓ {filename} is valid JSON")
        return True
    except json.JSONDecodeError as e:
        print(f"✗ {filename} has JSON error: {e}")
        return False
    except Exception as e:
        print(f"✗ {filename} error: {e}")
        return False

if __name__ == "__main__":
    files = [
        "frontend3/i18n/locales/en.json",
        "frontend3/i18n/locales/de.json"
    ]
    
    all_valid = True
    for file in files:
        if not validate_file(file):
            all_valid = False
    
    if all_valid:
        print("\nAll files are valid JSON.")
    else:
        print("\nSome files have JSON errors.")
        sys.exit(1)