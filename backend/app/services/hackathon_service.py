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


class HackathonService:
    """Service for hackathon-related business logic."""
    
    def __init__(self):
        self.hackathon_repo = HackathonRepository()
        self.registration_repo = HackathonRegistrationRepository()
        self.user_repo = UserRepository()
    
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
        hackathon_data["created_by"] = creator_id
        hackathon_data["status"] = "upcoming"
        
        hackathon = self.hackathon_repo.create(db, hackathon_data)
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
        
        self.hackathon_repo.delete(db, hackathon_id)
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
        registration = self.registration_repo.create(db, registration_data)
        return RegistrationSchema.model_validate(registration)
    
    def unregister_from_hackathon(
        self, db: Session, hackathon_id: int, user_id: int
    ) -> bool:
        """Unregister a user from a hackathon."""
        registration = self.registration_repo.get_by_hackathon_and_user(
            db, hackathon_id, user_id
        )
        if not registration:
            return False
        
        self.registration_repo.delete(db, registration.id)
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