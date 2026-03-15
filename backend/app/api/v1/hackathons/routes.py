"""
Hackathon API routes.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.auth import get_current_user
from app.core.permissions import (
    PERMISSION_CODES,
    can_delete_hackathon,
    can_manage_hackathon,
    can_manage_hackathon_reports,
    can_manage_team_reports_for_hackathon,
    user_has_permission,
)
from app.domain.schemas.hackathon import (
    Hackathon, HackathonCreate, HackathonUpdate, HackathonRegistrationStatus
)
from app.domain.schemas.report import Report, ReportCreateRequest
from app.domain.schemas.team import TeamReport
from app.repositories.hackathon_repository import (
    HackathonRepository,
    HackathonRegistrationRepository
)
from app.services.team_service import team_service
from app.services.report_service import report_service

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

    # Increment view count
    hackathon.view_count = (hackathon.view_count or 0) + 1
    db.commit()
    db.refresh(hackathon)

    return hackathon


@router.post("", response_model=Hackathon)
async def create_hackathon(
    hackathon: HackathonCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Create a new hackathon."""
    if not user_has_permission(db, current_user, PERMISSION_CODES["hackathons_create"]):
        raise HTTPException(status_code=403, detail="Not authorized to create hackathons")
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

    if not can_manage_hackathon(db, current_user, hackathon):
        raise HTTPException(status_code=403, detail="Not authorized to update this hackathon")

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

    if not can_delete_hackathon(db, current_user, hackathon):
        raise HTTPException(status_code=403, detail="Not authorized to delete this hackathon")

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


@router.get(
    "/{hackathon_id}/register",
    response_model=HackathonRegistrationStatus
)
async def check_hackathon_registration(
    hackathon_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Check if the current user is registered for a hackathon."""
    # Check if hackathon exists
    hackathon = hackathon_repository.get(db, hackathon_id)
    if not hackathon:
        raise HTTPException(status_code=404, detail="Hackathon not found")

    # Check if user is registered
    is_registered = registration_repository.is_user_registered(
        db, current_user.id, hackathon_id
    )

    response_data = {
        "is_registered": is_registered,
        "hackathon_id": hackathon_id,
        "user_id": current_user.id
    }

    # If registered, get registration details
    if is_registered:
        registration = db.query(registration_repository.model).filter(
            registration_repository.model.user_id == current_user.id,
            registration_repository.model.hackathon_id == hackathon_id
        ).first()
        if registration:
            response_data.update({
                "registration_id": registration.id,
                "status": registration.status,
                "registered_at": registration.registered_at
            })

    return response_data


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
            "title": project.title,
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
    from app.domain.models.team import Team, TeamMember
    teams = db.query(Team).filter(
        Team.hackathon_id == hackathon_id
    ).all()

    # Convert to simple dict representation
    team_list = []
    for team in teams:
        # Count team members
        member_count = db.query(TeamMember).filter(
            TeamMember.team_id == team.id
        ).count()

        team_list.append({
            "id": team.id,
            "name": team.name,
            "description": team.description,
            "owner_id": team.created_by,
            "created_at": team.created_at,
            "is_open": team.is_open if hasattr(team, 'is_open') else True,
            "max_members": (
                team.max_members if hasattr(team, 'max_members') else 5
            ),
            "member_count": member_count
        })

    return {"teams": team_list, "hackathon_id": hackathon_id}


@router.post("/{hackathon_id}/reports", response_model=Report)
async def report_hackathon(
    hackathon_id: int,
    payload: ReportCreateRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    hackathon = hackathon_repository.get(db, hackathon_id)
    if not hackathon:
        raise HTTPException(status_code=404, detail="Hackathon not found")
    if not user_has_permission(db, current_user, PERMISSION_CODES["reports_create"]):
        raise HTTPException(status_code=403, detail="Not authorized to create reports")
    try:
        return report_service.create_report(
            db,
            reporter_id=current_user.id,
            resource_type="hackathon",
            resource_id=hackathon_id,
            reason=payload.reason,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/{hackathon_id}/reports", response_model=List[Report])
async def get_hackathon_reports(
    hackathon_id: int,
    status: str | None = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    hackathon = hackathon_repository.get(db, hackathon_id)
    if not hackathon:
        raise HTTPException(status_code=404, detail="Hackathon not found")
    if not can_manage_hackathon_reports(db, current_user, hackathon_id):
        raise HTTPException(status_code=403, detail="Not authorized to view reports for this hackathon")
    return report_service.list_reports_for_resource(
        db, resource_type="hackathon", resource_id=hackathon_id, status=status, skip=skip, limit=limit
    )


@router.get("/{hackathon_id}/team-reports", response_model=List[TeamReport])
async def get_hackathon_team_reports(
    hackathon_id: int,
    status: str | None = None,
    team_id: int | None = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Get team reports for a hackathon for owners, moderators, admins, or superusers."""
    hackathon = hackathon_repository.get(db, hackathon_id)
    if not hackathon:
        raise HTTPException(status_code=404, detail="Hackathon not found")
    if not can_manage_team_reports_for_hackathon(db, current_user, hackathon_id):
        raise HTTPException(status_code=403, detail="Not authorized to view team reports for this hackathon")
    return team_service.list_hackathon_team_reports(
        db, hackathon_id=hackathon_id, status=status, team_id=team_id, skip=skip, limit=limit
    )
