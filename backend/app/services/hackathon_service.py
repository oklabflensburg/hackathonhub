"""
Hackathon service layer for business logic operations.
"""
from typing import Optional, List
from datetime import datetime
from sqlalchemy.orm import Session

from app.domain.schemas.hackathon import (
    HackathonCreate, HackathonUpdate, Hackathon as HackathonSchema,
    HackathonRegistration as RegistrationSchema
)
from app.repositories.hackathon_repository import (
    HackathonRepository, HackathonRegistrationRepository
)
from app.repositories.user_repository import UserRepository
from app.services.notification_service import NotificationService


class HackathonService:
    """Service for hackathon-related business logic."""

    def __init__(self):
        self.hackathon_repo = HackathonRepository()
        self.registration_repo = HackathonRegistrationRepository()
        self.user_repo = UserRepository()
        self.notification_service = NotificationService()

    def get_hackathons(
        self, db: Session, skip: int = 0, limit: int = 100
    ) -> List[HackathonSchema]:
        """Get all hackathons."""
        hackathons = self.hackathon_repo.get_all(db, skip=skip, limit=limit)
        return [HackathonSchema.model_validate(h) for h in hackathons]

    def get_hackathon(
        self, db: Session, hackathon_id: int
    ) -> Optional[HackathonSchema]:
        """Get a hackathon by ID."""
        hackathon = self.hackathon_repo.get(db, hackathon_id)
        if hackathon:
            return HackathonSchema.model_validate(hackathon)
        return None

    def create_hackathon(
        self, db: Session, hackathon_create: HackathonCreate, creator_id: int
    ) -> HackathonSchema:
        """Create a new hackathon."""
        # Business logic: set creator and initial status
        hackathon_data = hackathon_create.model_dump()
        hackathon_data["owner_id"] = creator_id
        hackathon_data["status"] = "upcoming"

        hackathon = self.hackathon_repo.create(db, obj_in=hackathon_data)
        return HackathonSchema.model_validate(hackathon)

    def update_hackathon(
        self, db: Session, hackathon_id: int, hackathon_update: HackathonUpdate
    ) -> Optional[HackathonSchema]:
        """Update a hackathon."""
        hackathon = self.hackathon_repo.get(db, hackathon_id)
        if not hackathon:
            return None

        update_data = hackathon_update.model_dump(exclude_unset=True)
        updated_hackathon = self.hackathon_repo.update(
            db, hackathon, update_data
        )
        return HackathonSchema.model_validate(updated_hackathon)

    def delete_hackathon(self, db: Session, hackathon_id: int) -> bool:
        """Delete a hackathon."""
        hackathon = self.hackathon_repo.get(db, hackathon_id)
        if not hackathon:
            return False

        self.hackathon_repo.delete(db, id=hackathon_id)
        return True

    def register_for_hackathon(
        self, db: Session, hackathon_id: int, user_id: int
    ) -> Optional[RegistrationSchema]:
        """Register a user for a hackathon."""
        # Business logic: check if already registered
        existing_reg = self.registration_repo.get_by_hackathon_and_user(
            db, hackathon_id, user_id
        )
        if existing_reg:
            return RegistrationSchema.model_validate(existing_reg)

        # Business logic: check hackathon capacity and dates
        hackathon = self.hackathon_repo.get(db, hackathon_id)
        if not hackathon:
            return None

        # Check if registration is open
        now = datetime.utcnow()
        if (hackathon.registration_deadline and
                hackathon.registration_deadline < now):
            return None

        # Check capacity
        current_registrations = self.registration_repo.get_by_hackathon(
            db, hackathon_id
        )
        if (hackathon.max_participants and
                len(current_registrations) >= hackathon.max_participants):
            return None

        # Create registration
        registration_data = {
            "hackathon_id": hackathon_id,
            "user_id": user_id,
            "status": "registered"
        }
        registration = self.registration_repo.create(
            db, obj_in=registration_data)

        # Send registration confirmation email (fire and forget)
        try:
            user = self.user_repo.get(db, user_id)
            if user and user.email:
                # Get user's preferred language
                language = getattr(user, "language", None) or "en"
                if language == "auto":
                    language = "en"

                variables = {
                    "hackathon_name": hackathon.name,
                    "user_name": user.name or user.username,
                    "hackathon_date": (
                        hackathon.start_date.isoformat()
                        if hackathon.start_date else "TBD"
                    ),
                    "hackathon_url": (
                        f"#TODO/hackathons/{hackathon_id}"  # TODO: Actual URL
                    )
                }

                self.notification_service.send_multi_channel_notification(
                    db=db,
                    notification_type="hackathon_registered",
                    user_id=user_id,
                    title=f"Registered for {hackathon.name}",
                    message=(
                        f"You have successfully registered for "
                        f"{hackathon.name}"
                    ),
                    language=language,
                    variables=variables
                )
        except Exception as e:
            # Log but don't fail registration
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"Failed to send hackathon registration email: {e}")

        return RegistrationSchema.model_validate(registration)

    def send_hackathon_start_reminders(self, db):
        """
        Send reminder emails for hackathons starting soon.
        This should be called by a scheduled job (e.g., cron).
        """
        import logging
        from datetime import datetime, timedelta
        from sqlalchemy import and_

        logger = logging.getLogger(__name__)

        # Find hackathons starting in the next 24 hours
        now = datetime.utcnow()
        # 23-25 hours from now
        reminder_window_start = now + timedelta(hours=23)
        reminder_window_end = now + timedelta(hours=25)

        # Get hackathons within the reminder window
        hackathons = self.hackathon_repo.get_all(
            db,
            filters=[
                and_(
                    self.hackathon_repo.model.start_date
                    >= reminder_window_start,
                    self.hackathon_repo.model.start_date
                    <= reminder_window_end,
                    self.hackathon_repo.model.status == "upcoming"
                )
            ]
        )

        if not hackathons:
            logger.info("No hackathons starting in the next 24 hours")
            return {"sent": 0, "errors": 0}

        sent_count = 0
        error_count = 0

        for hackathon in hackathons:
            # Get all registered users for this hackathon
            registrations = self.registration_repo.get_all(
                db,
                filters=[
                    self.registration_repo.model.hackathon_id == hackathon.id,
                    self.registration_repo.model.status == "registered"
                ]
            )

            for registration in registrations:
                try:
                    user = self.user_repo.get(db, registration.user_id)
                    if not user or not user.email:
                        continue

                    # Get user's preferred language
                    language = getattr(user, "language", None) or "en"
                    if language == "auto":
                        language = "en"

                    # Format start time
                    start_time = hackathon.start_date
                    if start_time:
                        time_str = start_time.strftime(
                            "%B %d, %Y at %H:%M UTC"
                        )
                    else:
                        time_str = "soon"

                    variables = {
                        "hackathon_name": hackathon.name,
                        "user_name": user.name or user.username,
                        "start_time": time_str,
                        "hackathon_url": f"#TODO/hackathons/{hackathon.id}",
                        "description": hackathon.description or "",
                        "location": hackathon.location or "Online"
                    }

                    self.notification_service.send_multi_channel_notification(
                        db=db,
                        notification_type="hackathon_start_reminder",
                        user_id=user.id,
                        title=f"{hackathon.name} starts soon!",
                        message=(
                            f"Reminder: {hackathon.name} starts {time_str}"
                        ),
                        language=language,
                        variables=variables
                    )

                    sent_count += 1

                except Exception as e:
                    logger.error(
                        f"Failed to send start reminder for hackathon "
                        f"{hackathon.id} to user {registration.user_id}: {e}"
                    )
                    error_count += 1

        logger.info(
            f"Sent {sent_count} hackathon start reminders with "
            f"{error_count} errors"
        )
        return {"sent": sent_count, "errors": error_count}

    def unregister_from_hackathon(
        self, db: Session, hackathon_id: int, user_id: int
    ) -> bool:
        """Unregister a user from a hackathon."""
        registration = self.registration_repo.get_by_hackathon_and_user(
            db, hackathon_id, user_id
        )
        if not registration:
            return False

        self.registration_repo.delete(db, id=registration.id)
        return True

    def get_hackathon_registrations(
        self, db: Session, hackathon_id: int
    ) -> List[RegistrationSchema]:
        """Get all registrations for a hackathon."""
        registrations = self.registration_repo.get_by_hackathon(
            db, hackathon_id
        )
        return [RegistrationSchema.model_validate(r) for r in registrations]

    def get_user_hackathons(
        self, db: Session, user_id: int
    ) -> List[HackathonSchema]:
        """Get all hackathons a user is registered for."""
        registrations = self.registration_repo.get_by_user(db, user_id)
        hackathons = []
        for reg in registrations:
            hackathon = self.hackathon_repo.get(db, reg.hackathon_id)
            if hackathon:
                hackathons.append(HackathonSchema.model_validate(hackathon))
        return hackathons

    def update_hackathon_status(
        self, db: Session, hackathon_id: int, status: str
    ) -> Optional[HackathonSchema]:
        """Update hackathon status (e.g., from 'upcoming' to 'active')."""
        hackathon = self.hackathon_repo.get(db, hackathon_id)
        if not hackathon:
            return None

        valid_statuses = ["upcoming", "active", "completed", "cancelled"]
        if status not in valid_statuses:
            return None

        hackathon.status = status
        db.commit()
        db.refresh(hackathon)
        return HackathonSchema.model_validate(hackathon)


# Global instance for dependency injection
hackathon_service = HackathonService()
