#!/usr/bin/env python3
"""
Migration script to clear base64 image data from database.
This script should be run before deploying the new file upload system.
"""

import sys
from pathlib import Path
from sqlalchemy.orm import Session

# Add the backend directory to the Python path
sys.path.append(str(Path(__file__).parent))

from database import get_db
import models


def clear_base64_images():
    """
    Clear base64 image data from database tables.
    This sets image_path, image_url, and banner_path fields to None
    if they contain base64 data URLs.
    """
    db: Session = next(get_db())
    
    try:
        # Clear base64 data from projects
        projects = db.query(models.Project).all()
        projects_cleared = 0
        for project in projects:
            if (project.image_path and 
                    project.image_path.startswith('data:image')):
                project.image_path = None
                projects_cleared += 1
        
        # Clear base64 data from hackathons
        hackathons = db.query(models.Hackathon).all()
        hackathons_cleared = 0
        for hackathon in hackathons:
            if (hackathon.image_url and 
                    hackathon.image_url.startswith('data:image')):
                hackathon.image_url = None
                hackathons_cleared += 1
            if (hackathon.banner_path and 
                    hackathon.banner_path.startswith('data:image')):
                hackathon.banner_path = None
                hackathons_cleared += 1
        
        db.commit()
        
        print("Migration completed successfully!")
        print(f"Projects cleared: {projects_cleared}")
        print(f"Hackathons cleared: {hackathons_cleared}")
        total_cleared = projects_cleared + hackathons_cleared
        print(f"Total records cleared: {total_cleared}")
        
        if total_cleared > 0:
            print("\nNote: Users will need to re-upload images.")
        
    except Exception as e:
        db.rollback()
        print(f"Error during migration: {e}")
        sys.exit(1)
    finally:
        db.close()


def check_base64_data():
    """
    Check how much base64 data exists in the database.
    """
    db: Session = next(get_db())
    
    try:
        # Check projects
        projects_with_base64 = db.query(models.Project).filter(
            models.Project.image_path.startswith('data:image')
        ).count()
        
        # Check hackathons
        hackathons_with_base64 = db.query(models.Hackathon).filter(
            (models.Hackathon.image_url.startswith('data:image')) |
            (models.Hackathon.banner_path.startswith('data:image'))
        ).count()
        
        total_base64 = projects_with_base64 + hackathons_with_base64
        
        print("Database base64 image data report:")
        print(f"Projects with base64 images: {projects_with_base64}")
        print(f"Hackathons with base64 images: {hackathons_with_base64}")
        print(f"Total records with base64: {total_base64}")
        
        if total_base64 == 0:
            print("\nNo base64 data found. Migration not needed.")
        else:
            estimate_kb = total_base64 * 100
            print(f"\nEstimated space to be freed: ~{estimate_kb}KB")
        
        return total_base64
        
    except Exception as e:
        print(f"Error checking database: {e}")
        return 0
    finally:
        db.close()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Migrate image data from base64 to file storage"
    )
    parser.add_argument(
        '--check',
        action='store_true',
        help='Check for base64 data without making changes'
    )
    parser.add_argument(
        '--migrate',
        action='store_true',
        help='Clear base64 data from database'
    )
    
    args = parser.parse_args()
    
    if not (args.check or args.migrate):
        parser.print_help()
        sys.exit(1)
    
    if args.check:
        print("Checking for base64 image data...")
        check_base64_data()
    
    if args.migrate:
        print("Clearing base64 image data...")
        print("WARNING: This will remove base64 image data.")
        print("Users will need to re-upload images.")
        print()
        
        # Ask for confirmation
        response = input("Are you sure you want to continue? (yes/no): ")
        if response.lower() != 'yes':
            print("Migration cancelled.")
            sys.exit(0)
        
        clear_base64_images()