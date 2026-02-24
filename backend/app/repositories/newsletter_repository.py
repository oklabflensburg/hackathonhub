"""
Newsletter subscription repository.
"""
from typing import Optional, Dict
from sqlalchemy.orm import Session

from app.domain.models.shared import NewsletterSubscription
from app.repositories.base import BaseRepository


class NewsletterRepository(BaseRepository[NewsletterSubscription]):
    """Repository for newsletter subscription operations."""

    def __init__(self):
        super().__init__(NewsletterSubscription)

    def get_by_email(
        self, db: Session, email: str
    ) -> Optional[NewsletterSubscription]:
        """Get a newsletter subscription by email address."""
        return db.query(self.model).filter(
            self.model.email == email.lower()
        ).first()

    def subscribe(
        self, db: Session, *, email: str, source: str = "website"
    ) -> NewsletterSubscription:
        """
        Subscribe an email to the newsletter with atomic duplicate prevention.

        If the email is already subscribed and active, returns the existing
        subscription. If the email was previously unsubscribed, reactivates it.
        Otherwise, creates a new subscription.
        """
        email_lower = email.lower()

        # Check for existing subscription
        existing = self.get_by_email(db, email_lower)

        if existing:
            if existing.is_active:
                # Already subscribed and active
                return existing
            else:
                # Previously unsubscribed, reactivate
                return self.update(
                    db,
                    db_obj=existing,
                    obj_in={
                        "is_active": True,
                        "unsubscribed_at": None,
                        "source": source
                    }
                )

        # Create new subscription
        return self.create(
            db,
            obj_in={
                "email": email_lower,
                "source": source,
                "is_active": True
            }
        )

    def unsubscribe(
        self, db: Session, email: str
    ) -> Optional[NewsletterSubscription]:
        """
        Unsubscribe an email from the newsletter.

        Returns the updated subscription if found, None otherwise.
        """
        from datetime import datetime

        subscription = self.get_by_email(db, email)
        if not subscription:
            return None

        return self.update(
            db,
            db_obj=subscription,
            obj_in={
                "is_active": False,
                "unsubscribed_at": datetime.utcnow()
            }
        )

    def get_active_subscriptions(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> list[NewsletterSubscription]:
        """Get all active newsletter subscriptions."""
        return db.query(self.model).filter(
            self.model.is_active.is_(True)
        ).offset(skip).limit(limit).all()

    def get_subscription_count(self, db: Session) -> Dict[str, int]:
        """Get counts of total and active subscriptions."""
        total = db.query(self.model).count()
        active = db.query(self.model).filter(
            self.model.is_active.is_(True)
        ).count()

        return {
            "total": total,
            "active": active,
            "inactive": total - active
        }
