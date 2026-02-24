"""
Team service layer for business logic operations.
"""
from typing import Optional, List
from sqlalchemy.orm import Session

from app.domain.schemas.team import (
    TeamCreate, TeamUpdate, Team as TeamSchema,
    TeamMember as TeamMemberSchema, TeamInvitation as TeamInvitationSchema,
    TeamInvitationCreate
)
from app.repositories.team_repository import (
    TeamRepository, TeamMemberRepository, TeamInvitationRepository
)
from app.repositories.user_repository import UserRepository


class TeamService:
    """Service for team-related business logic."""

    def __init__(self):
        self.team_repo = TeamRepository()
        self.member_repo = TeamMemberRepository()
        self.invitation_repo = TeamInvitationRepository()
        self.user_repo = UserRepository()

    def get_teams(
        self, db: Session, skip: int = 0, limit: int = 100
    ) -> List[TeamSchema]:
        """Get all teams."""
        teams = self.team_repo.get_all(db, skip=skip, limit=limit)
        return [TeamSchema.model_validate(t) for t in teams]

    def get_team(self, db: Session, team_id: int) -> Optional[TeamSchema]:
        """Get a team by ID."""
        team = self.team_repo.get(db, team_id)
        if team:
            return TeamSchema.model_validate(team)
        return None

    def create_team(
        self, db: Session, team_create: TeamCreate, creator_id: int
    ) -> TeamSchema:
        """Create a new team."""
        # Business logic: set creator
        team_data = team_create.model_dump()
        team_data["created_by"] = creator_id

        team = self.team_repo.create(db, obj_in=team_data)

        # Add creator as team member with admin role
        self.member_repo.create(db, obj_in={
            "team_id": team.id,
            "user_id": creator_id,
            "role": "admin",
            "status": "active"
        })

        return TeamSchema.model_validate(team)

    def update_team(
        self, db: Session, team_id: int, team_update: TeamUpdate
    ) -> Optional[TeamSchema]:
        """Update a team."""
        team = self.team_repo.get(db, team_id)
        if not team:
            return None

        update_data = team_update.model_dump(exclude_unset=True)
        updated_team = self.team_repo.update(
            db, db_obj=team, obj_in=update_data)
        return TeamSchema.model_validate(updated_team)

    def delete_team(self, db: Session, team_id: int) -> bool:
        """Delete a team."""
        team = self.team_repo.get(db, team_id)
        if not team:
            return False

        self.team_repo.delete(db, id=team_id)
        return True

    def get_team_members(
        self, db: Session, team_id: int
    ) -> List[TeamMemberSchema]:
        """Get all members of a team."""
        members = self.member_repo.get_team_members(db, team_id)
        return [TeamMemberSchema.model_validate(m) for m in members]

    def add_team_member(
        self, db: Session, team_id: int, user_id: int, role: str = "member"
    ) -> Optional[TeamMemberSchema]:
        """Add a member to a team."""
        # Business logic: check if already a member
        existing_member = self.member_repo.get_by_team_and_user(
            db, team_id, user_id
        )
        if existing_member:
            return TeamMemberSchema.model_validate(existing_member)

        # Create member
        member_data = {
            "team_id": team_id,
            "user_id": user_id,
            "role": role,
            "status": "active"
        }
        member = self.member_repo.create(db, obj_in=member_data)
        return TeamMemberSchema.model_validate(member)

    def remove_team_member(
        self, db: Session, team_id: int, user_id: int
    ) -> bool:
        """Remove a member from a team."""
        member = self.member_repo.get_by_team_and_user(db, team_id, user_id)
        if not member:
            return False

        # Business logic: prevent removing last admin
        if member.role == "admin":
            admin_members = [
                m for m in self.member_repo.get_team_members(db, team_id)
                if m.role == "admin"
            ]
            if len(admin_members) <= 1:
                return False

        self.member_repo.delete(db, id=member.id)
        return True

    def update_team_member_role(
        self, db: Session, team_id: int, user_id: int, role: str
    ) -> Optional[TeamMemberSchema]:
        """Update a team member's role."""
        member = self.member_repo.get_by_team_and_user(db, team_id, user_id)
        if not member:
            return None

        member.role = role
        db.commit()
        db.refresh(member)
        return TeamMemberSchema.model_validate(member)

    def create_team_invitation(
        self, db: Session, team_id: int, inviter_id: int,
        invitation_create: TeamInvitationCreate
    ) -> Optional[TeamInvitationSchema]:
        """Create a team invitation."""
        # Business logic: check if user is already a member
        existing_member = self.member_repo.get_by_team_and_user(
            db, team_id, invitation_create.invitee_id
        )
        if existing_member:
            return None

        # Check for existing pending invitation
        existing_invitation = self.invitation_repo.get_pending_by_team_and_user(
            db, team_id, invitation_create.invitee_id)
        if existing_invitation:
            return TeamInvitationSchema.model_validate(existing_invitation)

        # Create invitation
        invitation_data = invitation_create.model_dump()
        invitation_data["team_id"] = team_id
        invitation_data["inviter_id"] = inviter_id
        invitation_data["status"] = "pending"

        invitation = self.invitation_repo.create(db, obj_in=invitation_data)
        return TeamInvitationSchema.model_validate(invitation)

    def accept_team_invitation(
        self, db: Session, invitation_id: int, user_id: int
    ) -> Optional[TeamMemberSchema]:
        """Accept a team invitation."""
        invitation = self.invitation_repo.get(db, invitation_id)
        if not invitation or invitation.invitee_id != user_id:
            return None

        if invitation.status != "pending":
            return None

        # Update invitation status
        invitation.status = "accepted"
        db.commit()

        # Add user to team
        return self.add_team_member(
            db, invitation.team_id, user_id, role="member"
        )

    def decline_team_invitation(
        self, db: Session, invitation_id: int, user_id: int
    ) -> bool:
        """Decline a team invitation."""
        invitation = self.invitation_repo.get(db, invitation_id)
        if not invitation or invitation.invitee_id != user_id:
            return False

        if invitation.status != "pending":
            return False

        invitation.status = "declined"
        db.commit()
        return True

    def get_team_invitations(
        self, db: Session, team_id: int
    ) -> List[TeamInvitationSchema]:
        """Get all invitations for a team."""
        invitations = self.invitation_repo.get_by_team(db, team_id)
        return [TeamInvitationSchema.model_validate(i) for i in invitations]

    def get_user_teams(self, db: Session, user_id: int) -> List[TeamSchema]:
        """Get all teams a user is a member of."""
        memberships = self.member_repo.get_by_user(db, user_id)
        teams = []
        for membership in memberships:
            team = self.team_repo.get(db, membership.team_id)
            if team:
                teams.append(TeamSchema.model_validate(team))
        return teams


# Global instance for dependency injection
team_service = TeamService()
