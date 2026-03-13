"""
Team API routes.
"""
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, Request
from sqlalchemy import case, func
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.auth import get_current_user
from app.core.permissions import (
    PERMISSION_CODES,
    can_delete_team,
    can_manage_team,
    user_has_permission,
)
from app.domain.schemas.team import (
    Team, TeamCreate, TeamUpdate,
    TeamMember, TeamMemberCreateRequest,
    TeamInvitation, TeamInvitationCreateRequest,
    TeamReport, TeamReportCreateRequest
)
from app.domain.models.team import TeamMember as TeamMemberModel
from app.domain.schemas.project import Project
from app.domain.models.project import Project as ProjectModel
from app.repositories.team_repository import (
    TeamRepository,
    TeamMemberRepository,
    TeamInvitationRepository
)
from app.repositories.project_repository import ProjectRepository
from app.services.team_service import team_service
from app.i18n.dependencies import get_locale
from app.i18n.helpers import (
    raise_not_found, raise_forbidden, raise_bad_request,
    raise_internal_server_error
)

router = APIRouter()
team_repository = TeamRepository()
team_member_repository = TeamMemberRepository()
team_invitation_repository = TeamInvitationRepository()
project_repository = ProjectRepository()


def _calculate_engagement_score(
    member_count: int,
    project_count: int,
    view_count: int,
    last_activity_at: datetime | None,
) -> tuple[int, str]:
    """Calculate a stable team engagement score and level."""
    score = min(member_count * 12, 30) + min(project_count * 18, 30)
    score += min(view_count * 2, 25)

    if last_activity_at:
        now = datetime.now(timezone.utc)
        activity_time = last_activity_at
        if activity_time.tzinfo is None:
            activity_time = activity_time.replace(tzinfo=timezone.utc)
        age_days = max(0, (now - activity_time).days)
        if age_days <= 7:
            score += 15
        elif age_days <= 30:
            score += 8

    score = min(score, 100)

    if score >= 70:
        return score, "high"
    if score >= 35:
        return score, "medium"
    return score, "low"


def _attach_team_stats(db: Session, teams: List) -> None:
    """Populate aggregated team statistics used across team responses."""
    from app.domain.models.team import TeamMember

    team_ids = [team.id for team in teams]
    if not team_ids:
        return

    member_rows = db.query(
        TeamMember.team_id,
        func.count(TeamMember.id).label("member_count"),
    ).filter(
        TeamMember.team_id.in_(team_ids)
    ).group_by(TeamMember.team_id).all()
    member_map = {row.team_id: row.member_count for row in member_rows}

    project_rows = db.query(
        ProjectModel.team_id.label("team_id"),
        func.count(ProjectModel.id).label("project_count"),
        func.sum(
            case((ProjectModel.status == "active", 1), else_=0)
        ).label("active_project_count"),
        func.sum(
            case((ProjectModel.status == "completed", 1), else_=0)
        ).label("completed_project_count"),
        func.sum(ProjectModel.comment_count).label("total_comments"),
        func.sum(ProjectModel.upvote_count + ProjectModel.downvote_count).label("total_votes"),
        func.max(func.coalesce(ProjectModel.updated_at, ProjectModel.created_at)).label("last_activity_at"),
    ).filter(
        ProjectModel.team_id.in_(team_ids)
    ).group_by(ProjectModel.team_id).all()

    project_map = {
        row.team_id: {
            "project_count": row.project_count or 0,
            "active_project_count": row.active_project_count or 0,
            "completed_project_count": row.completed_project_count or 0,
            "total_comments": row.total_comments or 0,
            "total_votes": row.total_votes or 0,
            "last_activity_at": row.last_activity_at,
        }
        for row in project_rows
    }

    for team in teams:
        project_stats = project_map.get(team.id, {})
        member_count = member_map.get(team.id, 0)
        project_count = project_stats.get("project_count", 0)
        last_activity_at = project_stats.get("last_activity_at") or team.created_at
        view_count = team.view_count or 0
        engagement_score, engagement_level = _calculate_engagement_score(
            member_count=member_count,
            project_count=project_count,
            view_count=view_count,
            last_activity_at=last_activity_at,
        )

        team._member_count = member_count
        team.project_count = project_count
        team.active_project_count = project_stats.get("active_project_count", 0)
        team.completed_project_count = project_stats.get("completed_project_count", 0)
        team.total_comments = project_stats.get("total_comments", 0)
        team.total_votes = project_stats.get("total_votes", 0)
        team.last_activity_at = last_activity_at
        team.engagement_score = engagement_score
        team.engagement_level = engagement_level


@router.get("", response_model=List[Team])
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

    _attach_team_stats(db, teams)
    return teams


@router.get("/{team_id}", response_model=Team)
async def get_team(
    team_id: int,
    request: Request,
    db: Session = Depends(get_db),
    locale: str = Depends(get_locale)
):
    """Get a specific team by ID."""
    team = team_repository.get(db, team_id)
    if not team:
        raise_not_found(locale, "team")

    team.view_count = (team.view_count or 0) + 1
    db.commit()
    db.refresh(team)

    _attach_team_stats(db, [team])
    return team


@router.post("", response_model=Team)
async def create_team(
    team: TeamCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    locale: str = Depends(get_locale)
):
    """Create a new team."""
    if not user_has_permission(db, current_user, PERMISSION_CODES["teams_create"]):
        raise_forbidden(locale, "create", entity="team")
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
    current_user=Depends(get_current_user),
    locale: str = Depends(get_locale)
):
    """Update a team."""
    team = team_repository.get(db, team_id)
    if not team:
        raise_not_found(locale, "team")

    if not can_manage_team(db, current_user, team):
        raise_forbidden(locale, "update", entity="team")

    updated_team = team_repository.update(
        db, db_obj=team, obj_in=team_update.dict(exclude_unset=True)
    )
    return updated_team


@router.delete("/{team_id}")
async def delete_team(
    team_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    locale: str = Depends(get_locale)
):
    """Delete a team."""
    team = team_repository.get(db, team_id)
    if not team:
        raise_not_found(locale, "team")

    if not can_delete_team(db, current_user, team):
        raise_forbidden(locale, "delete", entity="team")

    success = team_repository.delete(db, id=team_id)
    if not success:
        raise_internal_server_error(locale, "delete", entity="team")

    return {"message": "Team deleted successfully"}


@router.get("/{team_id}/members", response_model=List[TeamMember])
async def get_team_members(
    team_id: int,
    db: Session = Depends(get_db),
    locale: str = Depends(get_locale)
):
    """Get members of a team."""
    # Check if team exists
    team = team_repository.get(db, team_id)
    if not team:
        raise_not_found(locale, "team")

    members = team_member_repository.get_team_members(db, team_id)
    return members


@router.get("/{team_id}/projects", response_model=List[Project])
async def get_team_projects(
    team_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    locale: str = Depends(get_locale)
):
    """Get projects belonging to a team."""
    # Check if team exists
    team = team_repository.get(db, team_id)
    if not team:
        raise_not_found(locale, "team")

    projects = project_repository.get_by_team(
        db, team_id, skip=skip, limit=limit
    )
    return projects


@router.post("/{team_id}/members", response_model=TeamMember)
async def add_team_member(
    team_id: int,
    member: TeamMemberCreateRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    locale: str = Depends(get_locale)
):
    """Add a member to a team."""
    # Verify team exists
    team = team_repository.get(db, team_id)
    if not team:
        raise_not_found(locale, "team")

    # Determine if this is a self-join request
    is_self_join = member.user_id == current_user.id

    if is_self_join:
        # Self-join allowed only if team is open
        if not team.is_open:
            raise_forbidden(locale, "team_not_open", entity="team")
        # Check if team has reached max members
        current_member_count = len(
            team_member_repository.get_team_members(db, team_id)
        )
        if current_member_count >= team.max_members:
            raise_bad_request(locale, "team_full", entity="team")
    else:
        # Adding another user requires owner/admin permission
        if not can_manage_team(db, current_user, team) and not user_has_permission(db, current_user, PERMISSION_CODES["teams_update_any"]):
            raise_forbidden(locale, "add_member", entity="team")

    # Check if user is already a member
    existing_member = team_member_repository.get_by_team_and_user(
        db, team_id, member.user_id)
    if existing_member:
        raise_bad_request(locale, "already_member", entity="team")

    # Create team member
    member_data = member.model_dump()
    # Ensure team_id matches URL parameter
    member_data["team_id"] = team_id

    db_member = team_member_repository.create(db, obj_in=member_data)
    return db_member


@router.post("/{team_id}/reports", response_model=TeamReport)
async def report_team(
    team_id: int,
    report: TeamReportCreateRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    locale: str = Depends(get_locale)
):
    """Report a team for moderator review."""
    team = team_repository.get(db, team_id)
    if not team:
        raise_not_found(locale, "team")

    if not user_has_permission(db, current_user, PERMISSION_CODES["team_reports_create"]):
        raise_forbidden(locale, "create", entity="report")

    reason = report.reason.strip()
    if not reason:
        raise_bad_request(locale, "invalid_request", entity="report")

    return team_service.create_team_report(
        db=db,
        team_id=team_id,
        reporter_id=current_user.id,
        reason=reason,
    )


@router.delete("/{team_id}/members/{user_id}")
async def remove_team_member(
    team_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    locale: str = Depends(get_locale)
):
    """Remove a member from a team."""
    # Verify team exists
    team = team_repository.get(db, team_id)
    if not team:
        raise_not_found(locale, "team")

    # Get target member first
    target_member = team_member_repository.get_by_team_and_user(
        db, team_id, user_id)
    if not target_member:
        raise_not_found(locale, "member")

    # Determine if this is a self-removal
    is_self_removal = user_id == current_user.id

    if is_self_removal:
        # Self-removal allowed for any member, but check if sole owner
        if target_member.role == "owner":
            # Count how many owners the team has
            from sqlalchemy import func
            owner_count = db.query(func.count(TeamMemberModel.id)).filter(
                TeamMemberModel.team_id == team_id,
                TeamMemberModel.role == "owner"
            ).scalar()
            if owner_count <= 1:
                raise_bad_request(
                    locale, "sole_owner_cannot_leave", entity="team"
                )
        # No further permission check needed for self-removal
    else:
        # Removing another user requires owner/admin permission
        current_user_member = team_member_repository.get_by_team_and_user(
            db, team_id, current_user.id)
        allowed_roles = ["owner", "admin"]
        has_permission = (current_user_member and
                          current_user_member.role in allowed_roles)
        if not has_permission:
            raise_forbidden(locale, "remove_member", entity="team")

        # Check if trying to remove team owner
        # (only if current user is also owner)
        if (target_member.role == "owner" and
                current_user_member.role != "owner"):
            raise_forbidden(locale, "remove_owner", entity="team")

    # Remove member
    team_member_repository.delete(db, id=target_member.id)

    return {"message": "Member removed successfully"}


@router.get("/{team_id}/invitations", response_model=List[TeamInvitation])
async def get_team_invitations(
    team_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    locale: str = Depends(get_locale)
):
    """Get invitations for a team."""
    # Check if team exists
    team = team_repository.get(db, team_id)
    if not team:
        raise_not_found(locale, "team")

    is_member = team_member_repository.is_user_member(db, team_id, current_user.id)
    if not is_member and not can_manage_team(db, current_user, team):
        raise_forbidden(locale, "view_invitations", entity="team")

    invitations = team_invitation_repository.get_team_invitations(db, team_id)
    return invitations


@router.post("/{team_id}/invitations", response_model=TeamInvitation)
async def create_team_invitation(
    team_id: int,
    invitation: TeamInvitationCreateRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    locale: str = Depends(get_locale)
):
    """Create an invitation to join a team."""
    # Verify team exists
    team = team_repository.get(db, team_id)
    if not team:
        raise_not_found(locale, "team")

    if not can_manage_team(db, current_user, team) and not user_has_permission(db, current_user, PERMISSION_CODES["team_invitations_create"]):
        raise_forbidden(locale, "create_invitation", entity="team")

    # Check if target user is already a team member
    existing_member = team_member_repository.get_by_team_and_user(
        db, team_id, invitation.invited_user_id)
    if existing_member:
        raise_bad_request(locale, "already_member", entity="team")

    # Check if invitation already exists
    existing_invitation = team_invitation_repository.get_by_team_and_user(
        db, team_id, invitation.invited_user_id)
    if existing_invitation:
        raise_bad_request(locale, "invitation_exists", entity="team")

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
    current_user=Depends(get_current_user),
    locale: str = Depends(get_locale)
):
    """Accept a team invitation."""
    # Get invitation
    invitation = team_invitation_repository.get(db, invitation_id)
    if not invitation:
        raise_not_found(locale, "invitation")

    # Verify invitation is for current user
    if invitation.invited_user_id != current_user.id:
        raise_forbidden(
            locale, "accept_others_invitation", entity="invitation"
        )

    # Check if invitation is still pending
    if invitation.status != "pending":
        raise_bad_request(
            locale, "invitation_already_processed", status=invitation.status
        )

    # Check if user is already a team member
    existing_member = team_member_repository.get_by_team_and_user(
        db, invitation.team_id, current_user.id)
    if existing_member:
        raise_bad_request(locale, "already_member", entity="team")

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
    current_user=Depends(get_current_user),
    locale: str = Depends(get_locale)
):
    """Decline a team invitation."""
    # Get invitation
    invitation = team_invitation_repository.get(db, invitation_id)
    if not invitation:
        raise_not_found(locale, "invitation")

    # Verify invitation is for current user
    if invitation.invited_user_id != current_user.id:
        raise_forbidden(
            locale, "decline_others_invitation", entity="invitation"
        )

    # Check if invitation is still pending
    if invitation.status != "pending":
        raise_bad_request(
            locale, "invitation_already_processed", status=invitation.status
        )

    # Update invitation status to declined
    invitation_update = {"status": "declined"}
    team_invitation_repository.update(
        db, db_obj=invitation, obj_in=invitation_update)

    return {"message": "Invitation declined", "invitation_id": invitation_id}


@router.delete("/invitations/{invitation_id}")
async def delete_team_invitation(
    invitation_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    locale: str = Depends(get_locale)
):
    """Delete/cancel a team invitation."""
    # Get invitation
    invitation = team_invitation_repository.get(db, invitation_id)
    if not invitation:
        raise_not_found(locale, "invitation")

    is_inviter = invitation.invited_by == current_user.id
    invitation_team = team_repository.get(db, invitation.team_id)
    if not (is_inviter or can_manage_team(db, current_user, invitation_team) or user_has_permission(db, current_user, PERMISSION_CODES["team_invitations_review"])):
        raise_forbidden(locale, "delete_invitation", entity="invitation")

    # Delete invitation
    success = team_invitation_repository.delete(db, id=invitation_id)
    if not success:
        raise_internal_server_error(locale, "delete", entity="invitation")

    return {
        "message": "Invitation deleted successfully",
        "invitation_id": invitation_id
    }
