"""
Team repository for database operations.
"""
from typing import List
from sqlalchemy.orm import Session

from app.repositories.base import BaseRepository
from app.domain.models.team import Team, TeamMember, TeamInvitation


class TeamRepository(BaseRepository[Team]):
    """Repository for teams."""
    
    def __init__(self):
        super().__init__(Team)
    
    def get_by_hackathon(
        self, db: Session, hackathon_id: int, skip: int = 0, limit: int = 100
    ) -> List[Team]:
        """Get teams by hackathon."""
        return db.query(self.model).filter(
            self.model.hackathon_id == hackathon_id
        ).order_by(
            self.model.created_at.desc()
        ).offset(skip).limit(limit).all()
    
    def get_by_creator(
        self, db: Session, creator_id: int, skip: int = 0, limit: int = 100
    ) -> List[Team]:
        """Get teams created by a user."""
        return db.query(self.model).filter(
            self.model.created_by == creator_id
        ).order_by(
            self.model.created_at.desc()
        ).offset(skip).limit(limit).all()


class TeamMemberRepository(BaseRepository[TeamMember]):
    """Repository for team members."""
    
    def __init__(self):
        super().__init__(TeamMember)
    
    def get_team_members(
        self, db: Session, team_id: int
    ) -> List[TeamMember]:
        """Get all members of a team."""
        return db.query(self.model).filter(
            self.model.team_id == team_id
        ).all()
    
    def get_user_teams(
        self, db: Session, user_id: int
    ) -> List[TeamMember]:
        """Get all teams a user belongs to."""
        return db.query(self.model).filter(
            self.model.user_id == user_id
        ).all()
    
    def is_user_member(
        self, db: Session, team_id: int, user_id: int
    ) -> bool:
        """Check if a user is a member of a team."""
        member = db.query(self.model).filter(
            self.model.team_id == team_id,
            self.model.user_id == user_id
        ).first()
        return member is not None


class TeamInvitationRepository(BaseRepository[TeamInvitation]):
    """Repository for team invitations."""
    
    def __init__(self):
        super().__init__(TeamInvitation)
    
    def get_team_invitations(
        self, db: Session, team_id: int
    ) -> List[TeamInvitation]:
        """Get all invitations for a team."""
        return db.query(self.model).filter(
            self.model.team_id == team_id,
            self.model.status == "pending"
        ).all()
    
    def get_user_invitations(
        self, db: Session, user_id: int
    ) -> List[TeamInvitation]:
        """Get all invitations for a user."""
        return db.query(self.model).filter(
            self.model.invited_user_id == user_id,
            self.model.status == "pending"
        ).all()