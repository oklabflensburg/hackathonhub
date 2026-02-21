#!/usr/bin/env python3
"""Test notification creation"""
import sys
sys.path.append('.')

from database import SessionLocal
import crud
import schemas
from datetime import datetime

# Create a test notification
db = SessionLocal()

try:
    # Create a test notification
    notification_data = {
        "user_id": 1,
        "notification_type": "test_notification",
        "title": "Test Notification",
        "message": "This is a test notification to verify the system works.",
        "data": {"test": True, "timestamp": str(datetime.utcnow())}
    }
    
    notification = crud.create_user_notification(
        db=db,
        user_id=1,
        notification_type="test_notification",
        title="Test Notification",
        message="This is a test notification to verify the system works.",
        data={"test": True, "timestamp": str(datetime.utcnow())}
    )
    
    print(f"Created notification: {notification.id}")
    print(f"Title: {notification.title}")
    print(f"Message: {notification.message}")
    print(f"Created at: {notification.created_at}")
    print(f"Read at: {notification.read_at}")
    
    # Get user notifications
    notifications = crud.get_user_notifications(db, user_id=1)
    print(f"\nTotal notifications for user: {len(notifications)}")
    
    unread_notifications = crud.get_user_notifications(db, user_id=1, unread_only=True)
    print(f"Unread notifications: {len(unread_notifications)}")
    
    # Mark as read
    if unread_notifications:
        marked = crud.mark_notification_as_read(db, unread_notifications[0].id)
        print(f"\nMarked notification {marked.id} as read at {marked.read_at}")
    
    # Get unread count again
    unread_after = crud.get_user_notifications(db, user_id=1, unread_only=True)
    print(f"Unread notifications after marking: {len(unread_after)}")
    
    print("\n✅ Notification system test completed successfully!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    db.close()