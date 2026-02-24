"""
User API routes.
"""
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.auth import get_current_user
from app.domain.schemas.user import User, UserUpdate
from app.domain.schemas.project import Project
from app.services.user_service import UserService
from app.domain.models.team import Team, TeamMember
from app.i18n.dependencies import get_locale
from app.i18n.helpers import (
    raise_not_found, raise_forbidden
)

router = APIRouter()


@router.get("", response_model=list[User])
async def get_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all users."""
    user_service = UserService(db)
    return user_service.get_users(skip=skip, limit=limit)


@router.get("/me", response_model=User)
async def get_current_user_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get current authenticated user profile."""
    # The current_user dependency already gives us the user
    return current_user


@router.patch("/me", response_model=User)
async def update_current_user_profile(
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    locale: str = Depends(get_locale)
):
    """Update current user's profile."""
    user_service = UserService()
    updated_user = user_service.update_user(
        db, user_id=current_user.id, user_update=user_update
    )
    if not updated_user:
        raise_not_found(locale, "user")
    return updated_user


@router.get("/me/stats")
async def get_user_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get user statistics"""
    # Count user's projects
    from app.domain.models.project import Project
    projects_count = db.query(Project).filter(
        Project.owner_id == current_user.id
    ).count()

    # Count user's hackathons (where user is owner)
    from app.domain.models.hackathon import Hackathon
    hackathons_count = db.query(Hackathon).filter(
        Hackathon.owner_id == current_user.id
    ).count()

    # Count user's votes
    from app.domain.models.project import Vote
    votes_count = db.query(Vote).filter(
        Vote.user_id == current_user.id
    ).count()

    return {
        "hackathonsCreated": hackathons_count,
        "projectsSubmitted": projects_count,
        "totalVotes": votes_count
    }


@router.get("/me/projects", response_model=List[Project])
async def get_user_projects(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all projects owned by the current user"""
    from app.repositories.project_repository import ProjectRepository
    project_repository = ProjectRepository()
    projects = project_repository.get_by_owner(
        db, owner_id=current_user.id
    )
    return projects


@router.get("/me/votes")
async def get_user_votes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all votes by the current user with project details"""
    from app.repositories.vote_repository import VoteRepository
    from app.repositories.project_repository import ProjectRepository

    vote_repository = VoteRepository()
    project_repository = ProjectRepository()

    votes = vote_repository.get_by_user(db, user_id=current_user.id)

    # Enrich votes with project details
    enriched_votes = []
    for vote in votes:
        # Get project details
        project = project_repository.get(db, vote.project_id)
        if project:
            # Get hackathon name if exists
            hackathon_name = None
            if project.hackathon:
                hackathon_name = project.hackathon.name

            # Get technologies as array
            technologies = []
            if project.technologies:
                tech_list = project.technologies.split(',')
                technologies = [
                    tech.strip() for tech in tech_list if tech.strip()
                ]

            # Calculate total votes
            total_votes = project.upvote_count + project.downvote_count

            # Prepare vote data
            vote_data = {
                "id": vote.id,
                "project_id": vote.project_id,
                "vote_type": vote.vote_type,
                "created_at": vote.created_at,
                "project_name": project.title,
                "project_description": project.description,
                "project_image": project.image_path,
                "project_technologies": technologies,
                "project_vote_count": total_votes,
                "project_comment_count": project.comment_count,
                "project_view_count": project.view_count,
                "hackathon_name": hackathon_name
            }

            # Add author name if available
            if project.owner:
                vote_data["project_author"] = project.owner.name
            else:
                vote_data["project_author"] = "Unknown"

            enriched_votes.append(vote_data)

    return enriched_votes


@router.get("/me/teams/{hackathon_id}")
async def get_user_teams_for_hackathon(
    hackathon_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    locale: str = Depends(get_locale)
):
    """Get teams that the current user belongs to for a specific hackathon"""
    # Check if hackathon exists
    from app.repositories.hackathon_repository import HackathonRepository

    hackathon_repository = HackathonRepository()

    hackathon = hackathon_repository.get(db, hackathon_id)
    if not hackathon:
        raise_not_found(locale, "hackathon")

    # Get user's teams for this hackathon
    # We need to query teams through TeamMember join
    teams = db.query(Team).join(
        TeamMember, Team.id == TeamMember.team_id
    ).filter(
        TeamMember.user_id == current_user.id,
        Team.hackathon_id == hackathon_id
    ).all()

    # Convert to TeamWithMembers schema
    from app.domain.models.user import User as UserModel

    result = []
    for team in teams:
        # Get members count
        member_count = db.query(TeamMember).filter(
            TeamMember.team_id == team.id
        ).count()

        # Create team with members data
        team_data = {
            "id": team.id,
            "name": team.name,
            "description": team.description,
            "hackathon_id": team.hackathon_id,
            "created_at": team.created_at,
            "member_count": member_count,
            "members": []
        }

        # Get team members
        members = db.query(TeamMember).filter(
            TeamMember.team_id == team.id
        ).all()

        for member in members:
            user = db.query(UserModel).filter(
                UserModel.id == member.user_id
            ).first()
            if user:
                team_data["members"].append({
                    "id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "role": member.role,
                    "joined_at": member.joined_at
                })

        result.append(team_data)

    return result


@router.get("/{user_id}/teams")
async def get_user_teams(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    locale: str = Depends(get_locale)
):
    """Get all teams a user belongs to"""
    # Check if user exists
    from app.repositories.user_repository import UserRepository
    from app.repositories.team_repository import TeamMemberRepository

    user_repository = UserRepository()
    team_member_repository = TeamMemberRepository()

    user = user_repository.get(db, user_id)
    if not user:
        raise_not_found(locale, "user")

    # Users can only view their own teams unless they're an admin
    if current_user.id != user_id:
        raise_forbidden(locale, "view_teams", entity="user")

    # Get user's team memberships
    team_memberships = team_member_repository.get_user_teams(
        db, user_id=user_id
    )

    # Get the actual teams
    teams = []
    for membership in team_memberships:
        team = db.query(Team).filter(Team.id == membership.team_id).first()
        if team:
            teams.append(team)

    # Convert to TeamWithMembers schema
    from app.domain.models.user import User as UserModel

    result = []
    for team in teams:
        # Get members count
        member_count = db.query(TeamMember).filter(
            TeamMember.team_id == team.id
        ).count()

        # Create team with members data
        team_data = {
            "id": team.id,
            "name": team.name,
            "description": team.description,
            "hackathon_id": team.hackathon_id,
            "created_at": team.created_at,
            "member_count": member_count,
            "members": []
        }

        # Get team members
        members = db.query(TeamMember).filter(
            TeamMember.team_id == team.id
        ).all()

        for member in members:
            user = db.query(UserModel).filter(
                UserModel.id == member.user_id
            ).first()
            if user:
                team_data["members"].append({
                    "id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "role": member.role,
                    "joined_at": member.joined_at
                })

        result.append(team_data)

    return result


@router.get("/{user_id}", response_model=User)
async def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    locale: str = Depends(get_locale)
):
    """Get a specific user by ID."""
    user_service = UserService(db)
    user = user_service.get_user(user_id)
    if user is None:
        raise_not_found(locale, "user")
    return user


@router.put("/{user_id}", response_model=User)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    locale: str = Depends(get_locale)
):
    """Update a user."""
    user_service = UserService(db)
    user = user_service.update_user(user_id, user_update)
    if user is None:
        raise_not_found(locale, "user")
    return user


@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    locale: str = Depends(get_locale)
):
    """Delete a user."""
    user_service = UserService(db)
    success = user_service.delete_user(user_id)
    if not success:
        raise_not_found(locale, "user")
    return {"message": "User deleted successfully"}


@router.get("/{user_id}/profile")
async def get_user_profile(
    user_id: int,
    db: Session = Depends(get_db),
    locale: str = Depends(get_locale)
):
    """Get user profile with additional information."""
    user_service = UserService(db)
    user = user_service.get_user(user_id)
    if user is None:
        raise_not_found(locale, "user")

    # Get user's projects
    from app.domain.models.project import Project
    projects = db.query(Project).filter(
        Project.owner_id == user_id
    ).limit(10).all()

    # Get user's team memberships
    team_memberships = db.query(TeamMember).filter(
        TeamMember.user_id == user_id
    ).all()

    # Get team details
    teams = []
    for membership in team_memberships:
        team = db.query(Team).filter(Team.id == membership.team_id).first()
        if team:
            teams.append({
                "id": team.id,
                "name": team.name,
                "role": membership.role,
                "joined_at": membership.joined_at
            })

    # Get hackathon registrations
    from app.domain.models.hackathon import HackathonRegistration
    registrations = db.query(HackathonRegistration).filter(
        HackathonRegistration.user_id == user_id
    ).all()

    hackathons = []
    for registration in registrations:
        from app.domain.models.hackathon import Hackathon
        hackathon = db.query(Hackathon).filter(
            Hackathon.id == registration.hackathon_id
        ).first()
        if hackathon:
            hackathons.append({
                "id": hackathon.id,
                "name": hackathon.name,
                "registered_at": registration.registered_at,
                "status": registration.status
            })

    return {
        "user": user,
        "projects": [
            {
                "id": p.id,
                "title": p.title,
                "description": p.description,
                "created_at": p.created_at
            } for p in projects
        ],
        "teams": teams,
        "hackathons": hackathons,
        "stats": {
            "project_count": len(projects),
            "team_count": len(teams),
            "hackathon_count": len(hackathons)
        }
    }
