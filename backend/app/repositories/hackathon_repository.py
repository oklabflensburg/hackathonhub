"""
Hackathon repository for database operations.
"""
from typing import List
from sqlalchemy.orm import Session

from app.repositories.base import BaseRepository
from app.domain.models.hackathon import Hackathon, HackathonRegistration


class HackathonRepository(BaseRepository[Hackathon]):
    """Repository for hackathons."""
    
    def __init__(self):
        super().__init__(Hackathon)
    
    def get_active_hackathons(
        self, db: Session, skip: int = 0, limit: int = 100
    ) -> List[Hackathon]:
        """Get active hackathons."""
        return db.query(self.model).filter(
            self.model.is_active.is_(True)
        ).order_by(
            self.model.start_date.desc()
        ).offset(skip).limit(limit).all()
    
    def get_by_owner(
        self, db: Session, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[Hackathon]:
        """Get hackathons by owner."""
        return db.query(self.model).filter(
            self.model.owner_id == owner_id
        ).order_by(
            self.model.created_at.desc()
        ).offset(skip).limit(limit).all()
    
    def search_by_name(
        self, db: Session, name_query: str, skip: int = 0, limit: int = 100
    ) -> List[Hackathon]:
        """Search hackathons by name."""
        return db.query(self.model).filter(
            self.model.name.ilike(f"%{name_query}%")
        ).order_by(
            self.model.name
        ).offset(skip).limit(limit).all()


class HackathonRegistrationRepository(BaseRepository[HackathonRegistration]):
    """Repository for hackathon registrations."""
    
    def __init__(self):
        super().__init__(HackathonRegistration)
    
    def get_user_registrations(
        self, db: Session, user_id: int
    ) -> List[HackathonRegistration]:
        """Get all hackathon registrations for a user."""
        return db.query(self.model).filter(
            self.model.user_id == user_id
        ).all()
    
    def get_hackathon_registrations(
        self, db: Session, hackathon_id: int
    ) -> List[HackathonRegistration]:
        """Get all registrations for a hackathon."""
        return db.query(self.model).filter(
            self.model.hackathon_id == hackathon_id
        ).all()
    
    def is_user_registered(
        self, db: Session, user_id: int, hackathon_id: int
    ) -> bool:
        """Check if a user is registered for a hackathon."""
        registration = db.query(self.model).filter(
            self.model.user_id == user_id,
            self.model.hackathon_id == hackathon_id
        ).first()
        return registration is not None
    
    def register_user(
        self, db: Session, user_id: int, hackathon_id: int
    ) -> HackathonRegistration:
        """Register a user for a hackathon."""
        # Check if already registered
        if self.is_user_registered(db, user_id, hackathon_id):
            raise ValueError("User already registered for this hackathon")
        
        registration = self.create(db, obj_in={
            "user_id": user_id,
            "hackathon_id": hackathon_id,
            "status": "registered"
        })
        
        # Update participant count
        hackathon = db.query(Hackathon).filter(
            Hackathon.id == hackathon_id
        ).first()
        if hackathon:
            hackathon.participant_count = (
                hackathon.participant_count + 1
                if hackathon.participant_count else 1
            )
            db.commit()
        
        return registration