"""
Current user (me) API routes.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.auth import get_current_user
from app.domain import schemas, models
from app.repositories.user_repository import UserRepository
from app.i18n.dependencies import get_locale
from app.i18n.helpers import raise_not_found

router = APIRouter()


@router.get("/me", response_model=schemas.UserWithDetails)
async def get_current_user(
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
    locale: str = Depends(get_locale)
):
    """Get current authenticated user with details
    including team memberships."""
    # Get user from database to ensure we have all relationships
    user_repo = UserRepository()
    db_user = user_repo.get(db, id=current_user.id)
    if not db_user:
        raise_not_found(locale, "user")

    # Convert to User schema first (avoids relationship errors)
    user_schema = schemas.User.from_orm(db_user)
    # Create UserWithDetails from User schema (extra fields will be None)
    user_with_details = schemas.UserWithDetails(**user_schema.model_dump())

    # Get user's team memberships
    team_memberships = db.query(models.TeamMember).filter(
        models.TeamMember.user_id == db_user.id
    ).all()

    # Convert team memberships to schema
    user_with_details.teams = []
    for membership in team_memberships:
        team_member_schema = schemas.TeamMember.from_orm(membership)
        # Include team details
        team = db.query(models.Team).filter(
            models.Team.id == membership.team_id
        ).first()
        if team:
            team_member_schema.team = schemas.Team.from_orm(team)
        user_with_details.teams.append(team_member_schema)

    # Get user's projects
    user_projects = db.query(models.Project).filter(
        models.Project.owner_id == db_user.id
    ).all()
    user_with_details.projects = [
        schemas.Project.from_orm(project) for project in user_projects
    ]

    # Get user's votes
    user_votes = db.query(models.Vote).filter(
        models.Vote.user_id == db_user.id
    ).all()
    user_with_details.votes = [
        schemas.Vote.from_orm(vote) for vote in user_votes
    ]

    # Get user's comments
    user_comments = db.query(models.Comment).filter(
        models.Comment.user_id == db_user.id
    ).all()
    user_with_details.comments = [
        schemas.Comment.from_orm(comment) for comment in user_comments
    ]

    # Get user's hackathon registrations
    user_registrations = db.query(models.HackathonRegistration).filter(
        models.HackathonRegistration.user_id == db_user.id
    ).all()
    user_with_details.hackathon_registrations = [
        schemas.HackathonRegistration.from_orm(reg)
        for reg in user_registrations
    ]

    return user_with_details


@router.get("/me/votes", response_model=List[schemas.Vote])
async def get_user_votes(
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
    locale: str = Depends(get_locale)
):
    """Get current user's votes."""
    # Get user's votes
    user_votes = db.query(models.Vote).filter(
        models.Vote.user_id == current_user.id
    ).all()
    
    return [schemas.Vote.from_orm(vote) for vote in user_votes]
