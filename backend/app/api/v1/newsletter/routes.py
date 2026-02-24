from fastapi import APIRouter, Header, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from app.core.database import get_db
from app.domain.schemas.newsletter import (
    NewsletterSubscribeRequest,
    NewsletterUnsubscribeRequest
)
from app.services.newsletter_service import newsletter_service

router = APIRouter()


@router.post("/subscribe")
async def subscribe_to_newsletter(
    request: NewsletterSubscribeRequest,
    idempotency_key: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    """Subscribe to newsletter with atomic duplicate prevention"""
    try:
        # Use the newsletter service to handle subscription
        result = newsletter_service.subscribe(
            db, email=request.email, source=request.source
        )
        
        subscription = result["subscription"]
        
        return {
            "message": "Successfully subscribed to newsletter",
            "email": subscription.email,
            "source": subscription.source,
            "already_subscribed": result["already_subscribed"],
            "subscribed_at": result["subscribed_at"],
            "welcome_email_sent": result["welcome_email_sent"]
        }
    except Exception as e:
        # Log the error and return a generic error message
        # In production, you'd want more specific error handling
        raise HTTPException(
            status_code=500,
            detail=f"Failed to subscribe to newsletter: {str(e)}"
        )


@router.post("/unsubscribe")
async def unsubscribe_from_newsletter(
    request: NewsletterUnsubscribeRequest,
    db: Session = Depends(get_db)
):
    """Unsubscribe from newsletter"""
    result = newsletter_service.unsubscribe(db, email=request.email)
    
    if not result:
        raise HTTPException(
            status_code=404,
            detail="Email not found in newsletter subscriptions"
        )
    
    subscription = result["subscription"]
    
    return {
        "message": "Successfully unsubscribed from newsletter",
        "email": subscription.email,
        "unsubscribed_at": result["unsubscribed_at"]
    }