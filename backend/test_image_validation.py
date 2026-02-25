#!/usr/bin/env python3
"""
Test image validation in Pydantic schemas.
"""
import sys
sys.path.insert(0, '.')

from app.domain.schemas.project import ProjectCreate, ProjectUpdate
from app.domain.schemas.hackathon import HackathonCreate, HackathonUpdate
from app.domain.schemas.user import UserBase, UserUpdate
from pydantic import ValidationError

def test_project_image_path():
    """Test that base64 data URLs are rejected for project image_path."""
    # Valid path should pass
    valid = ProjectCreate(
        title="Test Project",
        image_path="/static/uploads/projects/test.jpg"
    )
    assert valid.image_path == "/static/uploads/projects/test.jpg"
    
    # Base64 data URL should raise ValidationError
    try:
        ProjectCreate(
            title="Test Project",
            image_path="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
        )
        print("ERROR: Base64 data URL should have been rejected")
        return False
    except ValidationError as e:
        print("SUCCESS: Base64 data URL rejected")
        print(e.errors())
        return True

def test_hackathon_image_url():
    """Test that base64 data URLs are rejected for hackathon image_url."""
    # Valid path should pass
    valid = HackathonCreate(
        name="Test Hackathon",
        description="Test",
        start_date="2026-01-01T00:00:00",
        end_date="2026-01-02T00:00:00",
        location="Online",
        image_url="/static/uploads/hackathons/test.jpg"
    )
    assert valid.image_url == "/static/uploads/hackathons/test.jpg"
    
    # Base64 data URL should raise ValidationError
    try:
        HackathonCreate(
            name="Test Hackathon",
            description="Test",
            start_date="2026-01-01T00:00:00",
            end_date="2026-01-02T00:00:00",
            location="Online",
            image_url="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
        )
        print("ERROR: Base64 data URL should have been rejected")
        return False
    except ValidationError as e:
        print("SUCCESS: Base64 data URL rejected")
        print(e.errors())
        return True

def test_user_avatar_url():
    """Test that base64 data URLs are rejected for user avatar_url."""
    # Valid path should pass
    valid = UserBase(
        username="testuser",
        email="test@example.com",
        avatar_url="/static/uploads/avatars/test.jpg"
    )
    assert valid.avatar_url == "/static/uploads/avatars/test.jpg"
    
    # Base64 data URL should raise ValidationError
    try:
        UserBase(
            username="testuser",
            email="test@example.com",
            avatar_url="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
        )
        print("ERROR: Base64 data URL should have been rejected")
        return False
    except ValidationError as e:
        print("SUCCESS: Base64 data URL rejected")
        print(e.errors())
        return True

def test_null_values():
    """Test that null values are allowed."""
    # Project with null image_path
    project = ProjectCreate(title="Test", image_path=None)
    assert project.image_path is None
    
    # Hackathon with null image_url
    hackathon = HackathonCreate(
        name="Test",
        description="Test",
        start_date="2026-01-01T00:00:00",
        end_date="2026-01-02T00:00:00",
        location="Online",
        image_url=None
    )
    assert hackathon.image_url is None
    
    # User with null avatar_url
    user = UserBase(username="test", email="test@example.com", avatar_url=None)
    assert user.avatar_url is None
    print("SUCCESS: Null values allowed")
    return True

if __name__ == "__main__":
    print("Running image validation tests...")
    results = []
    results.append(test_project_image_path())
    results.append(test_hackathon_image_url())
    results.append(test_user_avatar_url())
    results.append(test_null_values())
    
    if all(results):
        print("\nAll tests passed!")
        sys.exit(0)
    else:
        print("\nSome tests failed!")
        sys.exit(1)