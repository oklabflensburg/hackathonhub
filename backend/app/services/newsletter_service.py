"""
Newsletter subscription service.
"""
from typing import Optional, Dict
from sqlalchemy.orm import Session

from app.domain.models.shared import NewsletterSubscription
from app.repositories.newsletter_repository import NewsletterRepository
from app.services.email_service import email_service


class NewsletterService:
    """Service for newsletter subscription operations."""

    def __init__(self):
        self.repository = NewsletterRepository()

    def subscribe(
        self, db: Session, email: str, source: str = "website"
    ) -> Dict:
        """
        Subscribe an email to the newsletter.
        
        Returns a dictionary with subscription details and status.
        """
        email_lower = email.lower()
        
        # Check if already subscribed
        existing = self.repository.get_by_email(db, email_lower)
        already_subscribed = existing and existing.is_active
        
        # Subscribe (handles duplicate prevention)
        subscription = self.repository.subscribe(
            db, email=email_lower, source=source
        )
        
        # Send welcome email if this is a new subscription
        welcome_email_sent = False
        if not already_subscribed:
            try:
                email_service.send_newsletter_welcome(
                    to_email=email_lower,
                    language="en"  # Default language, could be parameterized
                )
                welcome_email_sent = True
            except Exception as e:
                # Log error but don't fail the subscription
                # In production, you'd want to log this properly
                print(f"Failed to send welcome email to {email_lower}: {e}")
        
        return {
            "subscription": subscription,
            "already_subscribed": already_subscribed,
            "welcome_email_sent": welcome_email_sent,
            "subscribed_at": subscription.subscribed_at.isoformat()
            if subscription.subscribed_at else None
        }

    def unsubscribe(self, db: Session, email: str) -> Optional[Dict]:
        """
        Unsubscribe an email from the newsletter.
        
        Returns subscription details if found, None otherwise.
        """
        subscription = self.repository.unsubscribe(db, email)
        
        if not subscription:
            return None
        
        return {
            "subscription": subscription,
            "unsubscribed_at": subscription.unsubscribed_at.isoformat()
            if subscription.unsubscribed_at else None
        }

    def get_subscription_status(
        self, db: Session, email: str
    ) -> Optional[Dict]:
        """Get subscription status for an email."""
        subscription = self.repository.get_by_email(db, email)
        
        if not subscription:
            return None
        
        return {
            "email": subscription.email,
            "is_active": subscription.is_active,
            "subscribed_at": subscription.subscribed_at.isoformat()
            if subscription.subscribed_at else None,
            "unsubscribed_at": subscription.unsubscribed_at.isoformat()
            if subscription.unsubscribed_at else None,
            "source": subscription.source
        }

    def get_subscription_stats(self, db: Session) -> Dict[str, int]:
        """Get newsletter subscription statistics."""
        return self.repository.get_subscription_count(db)

    def get_active_subscribers(
        self, db: Session, skip: int = 0, limit: int = 100
    ) -> list[NewsletterSubscription]:
        """Get list of active subscribers."""
        return self.repository.get_active_subscriptions(
            db, skip=skip, limit=limit
        )


# Create a singleton instance
newsletter_service = NewsletterService()