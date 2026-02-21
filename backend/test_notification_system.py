#!/usr/bin/env python3
"""
Test script for the notification system.
"""
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Base
import models
from notification_service import notification_service


def setup_test_database():
    """Set up an in-memory SQLite database for testing."""
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False,
                                bind=engine)
    return SessionLocal()


def create_test_data(db):
    """Create test users, hackathon, and team."""
    # Create users
    user1 = models.User(
        username="testuser1",
        email="test1@example.com",
        name="Test User 1",
        is_active=True
    )
    user2 = models.User(
        username="testuser2",
        email="test2@example.com",
        name="Test User 2",
        is_active=True
    )
    user3 = models.User(
        username="testuser3",
        email="test3@example.com",
        name="Test User 3",
        is_active=True
    )
    
    db.add(user1)
    db.add(user2)
    db.add(user3)
    db.commit()
    db.refresh(user1)
    db.refresh(user2)
    db.refresh(user3)
    
    # Create hackathon
    hackathon = models.Hackathon(
        name="Test Hackathon",
        description="Test hackathon description",
        start_date="2024-01-01",
        end_date="2024-01-02",
        location="Test Location",
        is_active=True
    )
    db.add(hackathon)
    db.commit()
    db.refresh(hackathon)
    
    # Create team
    team = models.Team(
        name="Test Team",
        description="Test team description",
        hackathon_id=hackathon.id,
        max_members=5,
        is_open=True
    )
    db.add(team)
    db.commit()
    db.refresh(team)
    
    # Add user1 as team owner
    team_member = models.TeamMember(
        team_id=team.id,
        user_id=user1.id,
        role="owner"
    )
    db.add(team_member)
    db.commit()
    
    return {
        "user1": user1,
        "user2": user2,
        "user3": user3,
        "hackathon": hackathon,
        "team": team
    }


def test_notification_service():
    """Test the notification service."""
    print("Testing notification system...")
    
    # Set up test database
    db = setup_test_database()
    test_data = create_test_data(db)
    
    user1 = test_data["user1"]
    user2 = test_data["user2"]
    user3 = test_data["user3"]
    team = test_data["team"]
    
    print("Created test users:")
    print(f"  User 1: {user1.username} ({user1.email})")
    print(f"  User 2: {user2.username} ({user2.email})")
    print(f"  User 3: {user3.username} ({user3.email})")
    print(f"Created team: {team.name}")
    
    # Test 1: Send team invitation notification
    print("\nTest 1: Team invitation notification")
    print("Creating team invitation...")
    
    # Create invitation
    invitation = models.TeamInvitation(
        team_id=team.id,
        invited_user_id=user2.id,
        inviter_id=user1.id,
        status="pending"
    )
    db.add(invitation)
    db.commit()
    db.refresh(invitation)
    
    print(f"Created invitation ID: {invitation.id}")
    print("Sending invitation notification...")
    
    # Send notification
    success = notification_service.send_team_invitation_notification(
        db=db,
        invitation_id=invitation.id,
        language="en"
    )
    
    print(f"Notification sent: {success}")
    
    # Test 2: Send team member added notification
    print("\nTest 2: Team member added notification")
    print("Adding user3 to team...")
    
    # Add user3 to team
    team_member = models.TeamMember(
        team_id=team.id,
        user_id=user3.id,
        role="member"
    )
    db.add(team_member)
    db.commit()
    db.refresh(team_member)
    
    print("Added user3 to team as member")
    print("Sending member added notification...")
    
    # Send notification
    success = notification_service.send_team_member_added_notification(
        db=db,
        team_id=team.id,
        user_id=user3.id,
        added_by_id=user1.id,
        language="en"
    )
    
    print(f"Notification sent: {success}")
    
    # Test 3: Test generic notification sending
    print("\nTest 3: Generic notification")
    print("Sending generic notification...")
    
    success = notification_service.send_notification(
        notification_type="team_invitation_sent",
        recipient_email=user2.email,
        recipient_name=user2.name,
        language="en",
        variables={
            "team_name": team.name,
            "hackathon_name": "Test Hackathon",
            "actor_name": user1.name,
            "invitation_url": "http://localhost:3001/teams/1/invitations"
        }
    )
    
    print(f"Generic notification sent: {success}")
    
    # Test 4: Test German language notification
    print("\nTest 4: German language notification")
    
    success = notification_service.send_notification(
        notification_type="team_invitation_sent",
        recipient_email=user3.email,
        recipient_name=user3.name,
        language="de",
        variables={
            "team_name": team.name,
            "hackathon_name": "Test Hackathon",
            "actor_name": user1.name,
            "invitation_url": "http://localhost:3001/teams/1/invitations"
        }
    )
    
    print(f"German notification sent: {success}")
    
    print("\nAll tests completed!")
    note = "Note: Actual email sending depends on email service configuration."
    print(note)
    note2 = "If email service is not configured, notifications will be logged."
    print(note2)
    
    db.close()


if __name__ == "__main__":
    test_notification_service()