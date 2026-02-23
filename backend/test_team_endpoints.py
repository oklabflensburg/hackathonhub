#!/usr/bin/env python3
"""
Quick test script to verify team endpoints are working.
Run with: python test_team_endpoints.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi.testclient import TestClient
from app.main import app
from app.domain.models.team import Team, TeamMember, TeamInvitation
from app.core.database import SessionLocal, engine

# Create test client
client = TestClient(app)

def test_team_endpoints():
    """Test team endpoints"""
    print("Testing team endpoints...")
    
    # First, we need to authenticate (simplified test)
    # In a real test, we'd create a test user and get a token
    
    print("1. Testing GET /api/teams (requires auth)")
    response = client.get("/api/teams")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.text[:100]}...")
    
    print("\n2. Testing team model structure")
    # Check if Team model has expected fields
    team_attrs = dir(models.Team)
    expected_attrs = ['id', 'name', 'description', 'hackathon_id', 'max_members', 'is_open']
    for attr in expected_attrs:
        if hasattr(models.Team, attr):
            print(f"   ✓ Team model has attribute: {attr}")
        else:
            print(f"   ✗ Team model missing attribute: {attr}")
    
    print("\n3. Testing team member model structure")
    team_member_attrs = dir(models.TeamMember)
    expected_member_attrs = ['id', 'team_id', 'user_id', 'role', 'joined_at']
    for attr in expected_member_attrs:
        if hasattr(models.TeamMember, attr):
            print(f"   ✓ TeamMember model has attribute: {attr}")
        else:
            print(f"   ✗ TeamMember model missing attribute: {attr}")
    
    print("\n4. Testing team invitation model structure")
    invitation_attrs = dir(models.TeamInvitation)
    expected_invitation_attrs = ['id', 'team_id', 'invited_user_id', 'invited_by', 'status', 'created_at', 'expires_at']
    for attr in expected_invitation_attrs:
        if hasattr(models.TeamInvitation, attr):
            print(f"   ✓ TeamInvitation model has attribute: {attr}")
        else:
            print(f"   ✗ TeamInvitation model missing attribute: {attr}")
    
    print("\n5. Checking endpoint definitions in main.py")
    with open("main.py", "r") as f:
        content = f.read()
        
    endpoints_to_check = [
        ("GET /api/teams", "@app.get(\"/api/teams\""),
        ("GET /api/teams/{team_id}", "@app.get(\"/api/teams/{team_id}\""),
        ("POST /api/teams", "@app.post(\"/api/teams\""),
        ("PUT /api/teams/{team_id}", "@app.put(\"/api/teams/{team_id}\""),
        ("DELETE /api/teams/{team_id}", "@app.delete(\"/api/teams/{team_id}\""),
        ("GET /api/teams/{team_id}/members", "@app.get(\"/api/teams/{team_id}/members\""),
        ("POST /api/teams/{team_id}/members", "@app.post(\"/api/teams/{team_id}/members\""),
        ("DELETE /api/teams/{team_id}/members/{user_id}", "@app.delete(\"/api/teams/{team_id}/members/{user_id}\""),
        ("GET /api/me/invitations", "@app.get(\"/api/me/invitations\""),
        ("POST /api/invitations/{invitation_id}/accept", "@app.post(\"/api/invitations/{invitation_id}/accept\""),
        ("POST /api/invitations/{invitation_id}/decline", "@app.post(\"/api/invitations/{invitation_id}/decline\""),
    ]
    
    for endpoint_name, search_string in endpoints_to_check:
        if search_string in content:
            print(f"   ✓ {endpoint_name} endpoint defined")
        else:
            print(f"   ✗ {endpoint_name} endpoint NOT defined")
    
    print("\n6. Checking /api/me endpoint returns UserWithDetails")
    if "@app.get(\"/api/me\", response_model=schemas.UserWithDetails)" in content:
        print("   ✓ /api/me returns UserWithDetails (includes teams)")
    elif "@app.get(\"/api/me\", response_model=schemas.User)" in content:
        print("   ⚠ /api/me returns basic User (check if updated)")
    else:
        print("   ✗ /api/me endpoint not found")
    
    print("\nTest completed!")

if __name__ == "__main__":
    test_team_endpoints()