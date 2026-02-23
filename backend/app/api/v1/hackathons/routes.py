"""
Hackathon API routes.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.auth import get_current_user
from app.domain.schemas.hackathon import (
    Hackathon, HackathonCreate, HackathonUpdate
)
from app.repositories.hackathon_repository import (
    HackathonRepository,
    HackathonRegistrationRepository
)

router = APIRouter()
hackathon_repository = HackathonRepository()
registration_repository = HackathonRegistrationRepository()


@router.get("", response_model=List[Hackathon])
async def get_hackathons(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all hackathons."""
    hackathons = hackathon_repository.get_active_hackathons(
        db, skip=skip, limit=limit
    )
    return hackathons


@router.get("/{hackathon_id}", response_model=Hackathon)
async def get_hackathon(
    hackathon_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific hackathon by ID."""
    hackathon = hackathon_repository.get(db, hackathon_id)
    if not hackathon:
        raise HTTPException(status_code=404, detail="Hackathon not found")
    return hackathon


@router.post("", response_model=Hackathon)
async def create_hackathon(
    hackathon: HackathonCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Create a new hackathon."""
    hackathon_data = hackathon.dict()
    hackathon_data["owner_id"] = current_user.id
    new_hackathon = hackathon_repository.create(db, obj_in=hackathon_data)
    return new_hackathon


@router.put("/{hackathon_id}", response_model=Hackathon)
async def update_hackathon(
    hackathon_id: int,
    hackathon_update: HackathonUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Update a hackathon."""
    hackathon = hackathon_repository.get(db, hackathon_id)
    if not hackathon:
        raise HTTPException(status_code=404, detail="Hackathon not found")

    # Check ownership
    if hackathon.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized to update this hackathon"
        )

    updated_hackathon = hackathon_repository.update(
        db, db_obj=hackathon, obj_in=hackathon_update.dict(exclude_unset=True)
    )
    return updated_hackathon


@router.delete("/{hackathon_id}")
async def delete_hackathon(
    hackathon_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Delete a hackathon."""
    hackathon = hackathon_repository.get(db, hackathon_id)
    if not hackathon:
        raise HTTPException(status_code=404, detail="Hackathon not found")

    # Check ownership
    if hackathon.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized to delete this hackathon"
        )

    success = hackathon_repository.delete(db, id=hackathon_id)
    if not success:
        raise HTTPException(
            status_code=500, detail="Failed to delete hackathon"
        )

    return {"message": "Hackathon deleted successfully"}


@router.post("/{hackathon_id}/register")
async def register_for_hackathon(
    hackathon_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Register for a hackathon."""
    # Check if hackathon exists
    hackathon = hackathon_repository.get(db, hackathon_id)
    if not hackathon:
        raise HTTPException(status_code=404, detail="Hackathon not found")

    # Check if registration is open
    if not hackathon.registration_open:
        raise HTTPException(
            status_code=400,
            detail="Registration is closed for this hackathon"
        )

    # Check if user is already registered
    if registration_repository.is_user_registered(
        db, current_user.id, hackathon_id
    ):
        raise HTTPException(
            status_code=400,
            detail="Already registered for this hackathon"
        )

    # Register user
    try:
        registration = registration_repository.register_user(
            db, current_user.id, hackathon_id
        )
        return {
            "message": "Registered for hackathon",
            "hackathon_id": hackathon_id,
            "registration_id": registration.id
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{hackathon_id}/projects")
async def get_hackathon_projects(
    hackathon_id: int,
    db: Session = Depends(get_db)
):
    """Get projects for a hackathon."""
    # Check if hackathon exists
    hackathon = hackathon_repository.get(db, hackathon_id)
    if not hackathon:
        raise HTTPException(status_code=404, detail="Hackathon not found")

    # Import Project model and query projects
    from app.domain.models.project import Project
    projects = db.query(Project).filter(
        Project.hackathon_id == hackathon_id
    ).all()

    # Convert to simple dict representation
    project_list = []
    for project in projects:
        project_list.append({
            "id": project.id,
            "name": project.name,
            "description": project.description,
            "team_id": project.team_id,
            "created_at": project.created_at
        })

    return {"projects": project_list, "hackathon_id": hackathon_id}


@router.get("/{hackathon_id}/teams")
async def get_hackathon_teams(
    hackathon_id: int,
    db: Session = Depends(get_db)
):
    """Get teams for a hackathon."""
    # Check if hackathon exists
    hackathon = hackathon_repository.get(db, hackathon_id)
    if not hackathon:
        raise HTTPException(status_code=404, detail="Hackathon not found")

    # Import Team model and query teams
    from app.domain.models.team import Team
    teams = db.query(Team).filter(
        Team.hackathon_id == hackathon_id
    ).all()

    # Convert to simple dict representation
    team_list = []
    for team in teams:
        team_list.append({
            "id": team.id,
            "name": team.name,
            "description": team.description,
            "owner_id": team.created_by,
            "created_at": team.created_at
        })

    return {"teams": team_list, "hackathon_id": hackathon_id}
