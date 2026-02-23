"""
Notification types API routes.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories.notification_repository import (
    NotificationTypeRepository
)

router = APIRouter()
type_repository = NotificationTypeRepository()


@router.get("/")
async def get_notification_types(db: Session = Depends(get_db)):
    """Get all notification types."""
    try:
        notification_types = type_repository.get_all(db)
        
        # If no notification types exist, return empty list
        if not notification_types:
            return []
            
        return notification_types
    except Exception:
        # Log error and return empty list
        import logging
        logging.error("Error getting notification types")
        return []