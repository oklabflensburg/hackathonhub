"""
Team API routes.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.auth import get_current_user
from app.domain.schemas.team import (
    Team, TeamCreate, TeamUpdate,
    TeamMember, TeamMemberCreate,
    TeamInvitation, TeamInvitationCreate
)
from app.repositories.team_repository import (
    TeamRepository,
    TeamMemberRepository,
    TeamInvitationRepository
)

router = APIRouter()
team_repository = TeamRepository()
team_member_repository = TeamMemberRepository()
team_invitation_repository = TeamInvitationRepository()


@router.get("/", response_model=List[Team])
async def get_teams(
    skip: int = 0,
    limit: int = 100,
    hackathon_id: int = None,
    db: Session = Depends(get_db)
):
    """Get all teams."""
    if hackathon_id:
        # Get teams for specific hackathon
        teams = team_repository.get_by_hackathon(
            db, hackathon_id, skip=skip, limit=limit
        )
    else:
        # Get all teams
        teams = team_repository.get_multi(db, skip=skip, limit=limit)
    return teams


@router.get("/{team_id}", response_model=Team)
async def get_team(
    team_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific team by ID."""
    team = team_repository.get(db, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team


@router.post("/", response_model=Team)
async def create_team(
    team: TeamCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Create a new team."""
    team_data = team.dict()
    team_data["created_by"] = current_user.id
    
    # Create team
    new_team = team_repository.create(db, obj_in=team_data)
    
    # Add creator as team member with owner role
    team_member_repository.create(db, obj_in={
        "team_id": new_team.id,
        "user_id": current_user.id,
        "role": "owner"
    })
    
    return new_team


@router.put("/{team_id}", response_model=Team)
async def update_team(
    team_id: int,
    team_update: TeamUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Update a team."""
    team = team_repository.get(db, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    # Check if user is team owner
    is_owner = team_member_repository.is_user_member(
        db, team_id, current_user.id
    )
    if not is_owner:
        raise HTTPException(
            status_code=403,
            detail="Not authorized to update this team"
        )
    
    updated_team = team_repository.update(
        db, db_obj=team, obj_in=team_update.dict(exclude_unset=True)
    )
    return updated_team


@router.delete("/{team_id}")
async def delete_team(
    team_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Delete a team."""
    team = team_repository.get(db, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    # Check if user is team owner (creator)
    if team.created_by != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Only team creator can delete the team"
        )
    
    success = team_repository.delete(db, id=team_id)
    if not success:
        raise HTTPException(
            status_code=500, detail="Failed to delete team"
        )
    
    return {"message": "Team deleted successfully"}


@router.get("/{team_id}/members", response_model=List[TeamMember])
async def get_team_members(
    team_id: int,
    db: Session = Depends(get_db)
):
    """Get members of a team."""
    # Check if team exists
    team = team_repository.get(db, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    members = team_member_repository.get_team_members(db, team_id)
    return members


@router.post("/{team_id}/members", response_model=TeamMember)
async def add_team_member(
    team_id: int,
    member: TeamMemberCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Add a member to a team."""
    # Verify team exists
    team = team_repository.get(db, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    # Verify user is team owner or has permission
    # For now, just check if current user is team owner
    team_member = team_member_repository.get_by_team_and_user(
        db, team_id, current_user.id)
    if not team_member or team_member.role not in ["owner", "admin"]:
        raise HTTPException(
            status_code=403,
            detail="Only team owners or admins can add members"
        )
    
    # Check if user is already a member
    existing_member = team_member_repository.get_by_team_and_user(
        db, team_id, member.user_id)
    if existing_member:
        raise HTTPException(
            status_code=400,
            detail="User is already a member of this team"
        )
    
    # Create team member
    member_data = member.model_dump()
    # Ensure team_id matches URL parameter
    member_data["team_id"] = team_id
    
    db_member = team_member_repository.create(db, obj_in=member_data)
    return db_member


@router.delete("/{team_id}/members/{user_id}")
async def remove_team_member(
    team_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Remove a member from a team."""
    # Verify team exists
    team = team_repository.get(db, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    # Verify current user has permission (owner or admin)
    current_user_member = team_member_repository.get_by_team_and_user(
        db, team_id, current_user.id)
    allowed_roles = ["owner", "admin"]
    has_permission = (current_user_member and 
                      current_user_member.role in allowed_roles)
    if not has_permission:
        raise HTTPException(
            status_code=403,
            detail="Only team owners or admins can remove members"
        )
    
    # Check if trying to remove self
    if user_id == current_user.id:
        raise HTTPException(
            status_code=400,
            detail="Cannot remove yourself from team. Use leave team instead."
        )
    
    # Check if target user is a member
    target_member = team_member_repository.get_by_team_and_user(
        db, team_id, user_id)
    if not target_member:
        raise HTTPException(status_code=404, detail="Member not found")
    
    # Check if trying to remove team owner (only if current user is also owner)
    if target_member.role == "owner" and current_user_member.role != "owner":
        raise HTTPException(
            status_code=403,
            detail="Only team owner can remove another owner"
        )
    
    # Remove member
    team_member_repository.delete(db, id=target_member.id)
    
    return {"message": "Member removed successfully"}


@router.get("/{team_id}/invitations", response_model=List[TeamInvitation])
async def get_team_invitations(
    team_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Get invitations for a team."""
    # Check if team exists
    team = team_repository.get(db, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    # Check if user is team member
    is_member = team_member_repository.is_user_member(
        db, team_id, current_user.id
    )
    if not is_member:
        raise HTTPException(
            status_code=403,
            detail="Not authorized to view team invitations"
        )
    
    invitations = team_invitation_repository.get_team_invitations(db, team_id)
    return invitations


@router.post("/{team_id}/invitations", response_model=TeamInvitation)
async def create_team_invitation(
    team_id: int,
    invitation: TeamInvitationCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Create an invitation to join a team."""
    # Verify team exists
    team = team_repository.get(db, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    # Verify current user has permission (owner or admin)
    current_user_member = team_member_repository.get_by_team_and_user(
        db, team_id, current_user.id)
    allowed_roles = ["owner", "admin"]
    has_permission = (current_user_member and 
                      current_user_member.role in allowed_roles)
    if not has_permission:
        raise HTTPException(
            status_code=403,
            detail="Only team owners or admins can create invitations"
        )
    
    # Check if target user is already a team member
    existing_member = team_member_repository.get_by_team_and_user(
        db, team_id, invitation.user_id)
    if existing_member:
        raise HTTPException(
            status_code=400,
            detail="User is already a team member"
        )
    
    # Check if invitation already exists
    existing_invitation = team_invitation_repository.get_by_team_and_user(
        db, team_id, invitation.user_id)
    if existing_invitation:
        raise HTTPException(
            status_code=400,
            detail="Invitation already exists for this user"
        )
    
    # Create invitation
    invitation_data = invitation.model_dump()
    invitation_data["team_id"] = team_id
    invitation_data["invited_by"] = current_user.id
    
    db_invitation = team_invitation_repository.create(
        db, obj_in=invitation_data)
    return db_invitation


@router.post("/invitations/{invitation_id}/accept")
async def accept_team_invitation(
    invitation_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Accept a team invitation."""
    # Get invitation
    invitation = team_invitation_repository.get(db, invitation_id)
    if not invitation:
        raise HTTPException(status_code=404, detail="Invitation not found")
    
    # Verify invitation is for current user
    if invitation.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Cannot accept invitation for another user"
        )
    
    # Check if invitation is still pending
    if invitation.status != "pending":
        raise HTTPException(
            status_code=400,
            detail=f"Invitation is already {invitation.status}"
        )
    
    # Check if user is already a team member
    existing_member = team_member_repository.get_by_team_and_user(
        db, invitation.team_id, current_user.id)
    if existing_member:
        raise HTTPException(
            status_code=400,
            detail="User is already a team member"
        )
    
    # Add user to team as a regular member
    member_data = {
        "team_id": invitation.team_id,
        "user_id": current_user.id,
        "role": "member"
    }
    team_member_repository.create(db, obj_in=member_data)
    
    # Update invitation status
    invitation_update = {"status": "accepted"}
    team_invitation_repository.update(
        db, db_obj=invitation, obj_in=invitation_update)
    
    return {"message": "Invitation accepted", "invitation_id": invitation_id}


@router.post("/invitations/{invitation_id}/decline")
async def decline_team_invitation(
    invitation_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Decline a team invitation."""
    # Get invitation
    invitation = team_invitation_repository.get(db, invitation_id)
    if not invitation:
        raise HTTPException(status_code=404, detail="Invitation not found")
    
    # Verify invitation is for current user
    if invitation.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Cannot decline invitation for another user"
        )
    
    # Check if invitation is still pending
    if invitation.status != "pending":
        raise HTTPException(
            status_code=400,
            detail=f"Invitation is already {invitation.status}"
        )
    
    # Update invitation status to declined
    invitation_update = {"status": "declined"}
    team_invitation_repository.update(
        db, db_obj=invitation, obj_in=invitation_update)
    
    return {"message": "Invitation declined", "invitation_id": invitation_id}