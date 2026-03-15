"""Project API routes."""
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, Body, Request, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func
from typing import List, Optional

from app.core.database import get_db
from app.core.auth import get_current_user
from app.core.permissions import (
    PERMISSION_CODES,
    can_delete_project,
    can_manage_project,
    can_manage_project_reports,
    user_has_permission,
)
from app.domain.schemas.project import (
    Project, ProjectCreate, ProjectUpdate, CommentCreate, Comment
)
from app.domain.schemas.user import PublicUser
from app.domain.schemas.report import Report, ReportCreateRequest
from app.services.project_service import project_service
from app.repositories.project_repository import ProjectRepository
from app.repositories.project_repository import VoteRepository
from app.repositories.project_repository import CommentRepository
from app.domain.models.project import Vote as VoteModel, Comment as CommentModel
from app.i18n.dependencies import get_locale
from app.i18n.helpers import (
    raise_not_found, raise_bad_request,
    raise_internal_server_error
)
from app.i18n.translations import get_translation
from app.services.report_service import report_service

router = APIRouter()

# Initialize repository instances
project_repository = ProjectRepository()
vote_repository = VoteRepository()
comment_repository = CommentRepository()


def _serialize_comment(comment) -> Comment:
    """Serialize a comment including author and nested replies."""
    return Comment(
        id=comment.id,
        content=comment.content,
        user_id=comment.user_id,
        project_id=comment.project_id,
        parent_id=comment.parent_id,
        upvote_count=comment.upvote_count or 0,
        downvote_count=comment.downvote_count or 0,
        vote_score=comment.vote_score or 0,
        created_at=comment.created_at,
        updated_at=comment.updated_at,
        user=(
            PublicUser.model_validate(comment.user)
            if getattr(comment, "user", None) else None
        ),
        replies=[],
    )


def _build_comment_tree(db: Session, project_id: int) -> list[Comment]:
    """Build a nested comment tree for a project."""
    flat_comments = comment_repository.get_project_comments_flat(db, project_id)
    comment_map: dict[int, Comment] = {}
    root_comments: list[Comment] = []

    for db_comment in flat_comments:
        comment_map[db_comment.id] = _serialize_comment(db_comment)

    for db_comment in flat_comments:
        serialized = comment_map[db_comment.id]
        if db_comment.parent_id and db_comment.parent_id in comment_map:
            comment_map[db_comment.parent_id].replies.append(serialized)
        else:
            root_comments.append(serialized)

    root_comments.sort(key=lambda item: item.created_at, reverse=True)
    for root in root_comments:
        root.replies.sort(key=lambda item: item.created_at)

    return root_comments


def _calculate_project_engagement(
    total_votes: int,
    total_comments: int,
    view_count: int,
    last_activity_at: datetime | None,
) -> tuple[int, float, str]:
    """Calculate project engagement score, rate and level."""
    score = min(total_votes * 12, 40) + min(total_comments * 15, 35)
    score += min(view_count * 2, 15)

    if last_activity_at:
        now = datetime.now(timezone.utc)
        activity_time = last_activity_at
        if activity_time.tzinfo is None:
            activity_time = activity_time.replace(tzinfo=timezone.utc)
        age_days = max(0, (now - activity_time).days)
        if age_days <= 7:
            score += 10
        elif age_days <= 30:
            score += 5

    score = min(score, 100)

    interactions = total_votes + total_comments
    rate = round(min(100.0, (interactions / max(view_count, 1)) * 100), 1)

    if score >= 70 or rate >= 15:
        return score, rate, "high"
    if score >= 35 or rate >= 5:
        return score, rate, "medium"
    return score, rate, "low"


def _attach_project_stats(db: Session, projects: List[Project]) -> None:
    """Populate aggregated project engagement statistics."""
    project_ids = [project.id for project in projects]
    if not project_ids:
        return

    vote_rows = db.query(
        VoteModel.project_id,
        func.max(VoteModel.created_at).label("last_vote_at"),
    ).filter(
        VoteModel.project_id.in_(project_ids)
    ).group_by(VoteModel.project_id).all()
    vote_activity_map = {
        row.project_id: row.last_vote_at for row in vote_rows
    }

    comment_rows = db.query(
        CommentModel.project_id,
        func.max(CommentModel.created_at).label("last_comment_at"),
    ).filter(
        CommentModel.project_id.in_(project_ids)
    ).group_by(CommentModel.project_id).all()
    comment_activity_map = {
        row.project_id: row.last_comment_at for row in comment_rows
    }

    for project in projects:
        total_votes = (project.upvote_count or 0) + (project.downvote_count or 0)
        total_comments = project.comment_count or 0
        last_activity_candidates = [
            project.updated_at,
            project.created_at,
            vote_activity_map.get(project.id),
            comment_activity_map.get(project.id),
        ]
        last_activity_at = max(
            (candidate for candidate in last_activity_candidates if candidate is not None),
            default=project.created_at,
        )
        engagement_score, engagement_rate, engagement_level = _calculate_project_engagement(
            total_votes=total_votes,
            total_comments=total_comments,
            view_count=project.view_count or 0,
            last_activity_at=last_activity_at,
        )

        project.total_votes = total_votes
        project.total_comments = total_comments
        project.last_activity_at = last_activity_at
        project.engagement_score = engagement_score
        project.engagement_rate = engagement_rate
        project.engagement_level = engagement_level


@router.get("", response_model=List[Project])
async def get_projects(
    skip: int = 0,
    limit: int = 100,
    user: Optional[int] = None,
    technology: Optional[str] = None,
    technologies: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    locale: str = Depends(get_locale)
):
    """Get all projects, optionally filtered by user, technology, or search."""
    if search:
        projects = project_service.search_projects(
            db, search_term=search, skip=skip, limit=limit
        )
    elif technology:
        projects = project_service.get_projects_by_technology(
            db, technology=technology, skip=skip, limit=limit
        )
    elif technologies:
        tech_list = [t.strip() for t in technologies.split(",") if t.strip()]
        projects = project_service.get_projects_by_technologies(
            db, technologies=tech_list, skip=skip, limit=limit
        )
    elif user is not None:
        projects = project_service.get_projects(
            db, skip=skip, limit=limit, user_id=user
        )
    else:
        projects = project_service.get_projects(db, skip=skip, limit=limit)

    _attach_project_stats(db, projects)
    return projects


@router.get("/{project_id}", response_model=Project)
async def get_project(
    project_id: int,
    request: Request,
    db: Session = Depends(get_db),
    locale: str = Depends(get_locale)
):
    """Get a specific project by ID."""
    project = project_service.get_project(db, project_id)
    if not project:
        raise_not_found(locale, "project")
    _attach_project_stats(db, [project])
    return project


@router.post("", response_model=Project)
async def create_project(
    project: ProjectCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    locale: str = Depends(get_locale)
):
    """Create a new project."""
    if not user_has_permission(db, current_user, PERMISSION_CODES["projects_create"]):
        raise_bad_request(locale, "forbidden")
    new_project = project_service.create_project(
        db, project, current_user.id
    )
    return new_project


@router.put("/{project_id}", response_model=Project)
async def update_project(
    project_id: int,
    project_update: ProjectUpdate,
    request: Request,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    locale: str = Depends(get_locale)
):
    """Update a project."""
    project = project_repository.get(db, project_id)
    if project and not can_manage_project(db, current_user, project):
        from app.i18n.helpers import raise_forbidden
        raise_forbidden(locale, "update", entity="project")
    updated_project = project_service.update_project(
        db, project_id, project_update, current_user.id, locale
    )
    if not updated_project:
        raise_not_found(locale, "project")
    return updated_project


@router.delete("/{project_id}")
async def delete_project(
    project_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    locale: str = Depends(get_locale)
):
    """Delete a project."""
    project = project_repository.get(db, project_id)
    if project and not can_delete_project(db, current_user, project):
        from app.i18n.helpers import raise_forbidden
        raise_forbidden(locale, "delete", entity="project")
    success = project_service.delete_project(
        db, project_id, current_user.id, locale
    )
    if not success:
        raise_internal_server_error(locale, "delete", entity="project")

    message = get_translation("success.project_deleted", locale)
    return {"message": message}


@router.post("/{project_id}/reports", response_model=Report)
async def report_project(
    project_id: int,
    payload: ReportCreateRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    locale: str = Depends(get_locale),
):
    project = project_repository.get(db, project_id)
    if not project:
        raise_not_found(locale, "project")
    if not user_has_permission(db, current_user, PERMISSION_CODES["reports_create"]):
        raise HTTPException(status_code=403, detail="Not authorized to create reports")
    try:
        return report_service.create_report(
            db,
            reporter_id=current_user.id,
            resource_type="project",
            resource_id=project_id,
            reason=payload.reason,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/{project_id}/reports", response_model=List[Report])
async def get_project_reports(
    project_id: int,
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    locale: str = Depends(get_locale),
):
    project = project_repository.get(db, project_id)
    if not project:
        raise_not_found(locale, "project")
    if not can_manage_project_reports(db, current_user, project_id):
        raise HTTPException(
            status_code=403,
            detail="Not authorized to view reports for this project",
        )
    return report_service.list_reports_for_resource(
        db,
        resource_type="project",
        resource_id=project_id,
        status=status,
        skip=skip,
        limit=limit,
    )


@router.post("/{project_id}/vote")
async def vote_for_project(
    project_id: int,
    request: Request,
    # "upvote" or "downvote" from JSON body
    vote_type: str = Body(..., embed=True),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    locale: str = Depends(get_locale)
):
    """Vote for a project with proper concurrency handling."""
    # Normalize vote type
    vote_type = vote_type.lower().strip()

    # Map 'up'/'down' to 'upvote'/'downvote' for compatibility
    if vote_type == 'up':
        vote_type = 'upvote'
    elif vote_type == 'down':
        vote_type = 'downvote'

    # Validate vote type
    if vote_type not in ["upvote", "downvote"]:
        raise_bad_request(
            locale,
            validation_key="vote_type_must_be",
            option1="upvote",
            option2="downvote"
        )

    # Check if project exists
    project = project_repository.get(db, project_id)
    if not project:
        raise_not_found(locale, "project")

    try:
        # Check if user already voted
        existing_vote = vote_repository.get_user_vote_for_project(
            db, current_user.id, project_id
        )

        vote_obj = None

        if existing_vote:
            # Update existing vote
            if existing_vote.vote_type == vote_type:
                # Same vote type - remove the vote
                vote_repository.delete(db, id=existing_vote.id)
                message = f"Removed {vote_type}"
            else:
                # Change vote type
                existing_vote.vote_type = vote_type
                db.commit()
                db.refresh(existing_vote)
                message = f"Changed vote to {vote_type}"
                vote_obj = existing_vote
        else:
            # Create new vote with error handling for race conditions
            try:
                vote_obj = vote_repository.create(db, obj_in={
                    "user_id": current_user.id,
                    "project_id": project_id,
                    "vote_type": vote_type
                })
                message = f"Added {vote_type}"
            except IntegrityError:
                # Race condition: vote was created by another request
                db.rollback()
                # Get the current vote state
                existing_vote = vote_repository.get_user_vote_for_project(
                    db, current_user.id, project_id
                )
                if existing_vote:
                    # Another request created a vote, return current state
                    message = f"Already voted {existing_vote.vote_type}"
                    vote_type = existing_vote.vote_type
                    vote_obj = existing_vote
                else:
                    # Retry once (should rarely happen)
                    vote_obj = vote_repository.create(db, obj_in={
                        "user_id": current_user.id,
                        "project_id": project_id,
                        "vote_type": vote_type
                    })
                    message = f"Added {vote_type}"

    except IntegrityError:
        db.rollback()
        raise_bad_request(locale, "vote_conflict")

    # Update vote counts
    vote_repository.update_vote_counts(db, project_id)

    # Get updated project stats for frontend
    project = project_repository.get(db, project_id)
    db.refresh(project)

    response_data = {
        "message": message,
        "project_id": project_id,
        "vote_type": vote_type,
        "project_stats": {
            "project_id": project_id,
            "upvotes": getattr(project, 'upvote_count', 0),
            "downvotes": getattr(project, 'downvote_count', 0),
            "total_score": getattr(project, 'vote_score', 0),
            "user_vote": (
                vote_type
                if message.startswith("Added") or message.startswith("Changed")
                else None
            )
        }
    }

    # Include vote object if it exists (for frontend state updates)
    if vote_obj:
        response_data["vote"] = {
            "id": vote_obj.id,
            "user_id": vote_obj.user_id,
            "project_id": vote_obj.project_id,
            "vote_type": vote_obj.vote_type,
            "created_at": (
                vote_obj.created_at.isoformat()
                if vote_obj.created_at
                else None
            )
        }

    return response_data


@router.get("/{project_id}/vote-stats")
async def get_project_vote_stats(
    project_id: int,
    request: Request,
    db: Session = Depends(get_db),
    locale: str = Depends(get_locale)
):
    """Get vote statistics for a project (public endpoint)."""
    # Check if project exists
    project = project_repository.get(db, project_id)
    if not project:
        raise_not_found(locale, "project")

    # Note: user_vote will always be None for this public endpoint
    # The frontend should handle user-specific votes separately

    # Use getattr with default values in case columns don't exist yet
    # (e.g., before migration runs)
    upvotes = getattr(project, 'upvote_count', 0)
    downvotes = getattr(project, 'downvote_count', 0)
    vote_score = getattr(project, 'vote_score', 0)

    return {
        "project_id": project_id,
        "upvotes": upvotes,
        "downvotes": downvotes,
        "total_score": vote_score,
        "user_vote": None
    }


@router.post("/{project_id}/view")
async def increment_project_view(
    project_id: int,
    request: Request,
    db: Session = Depends(get_db),
    locale: str = Depends(get_locale)
):
    """Increment view count for a project"""
    # Check if project exists
    project = project_repository.get(db, project_id)
    if not project:
        raise_not_found(locale, "project")

    # Increment view count
    project.view_count = (project.view_count or 0) + 1
    db.commit()
    db.refresh(project)

    message = get_translation("success.view_count_incremented", locale)
    return {
        "message": message,
        "view_count": project.view_count
    }


@router.delete("/{project_id}/vote")
async def remove_vote(
    project_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    locale: str = Depends(get_locale)
):
    """Remove user's vote from a project."""
    # Check if project exists
    project = project_repository.get(db, project_id)
    if not project:
        raise_not_found(locale, "project")

    # Check if user has voted
    existing_vote = vote_repository.get_user_vote_for_project(
        db, current_user.id, project_id
    )
    if not existing_vote:
        raise_not_found(locale, "vote")

    # Delete the vote
    vote_repository.delete(db, id=existing_vote.id)

    # Update vote counts
    vote_repository.update_vote_counts(db, project_id)

    # Get updated project stats
    project = project_repository.get(db, project_id)
    db.refresh(project)  # Ensure we have latest values

    message = get_translation("success.vote_removed", locale)
    return {
        "message": message,
        "project_stats": {
            "project_id": project_id,
            "upvotes": getattr(project, 'upvote_count', 0),
            "downvotes": getattr(project, 'downvote_count', 0),
            "total_score": getattr(project, 'vote_score', 0),
            "user_vote": None
        }
    }


@router.get("/{project_id}/comments")
async def get_project_comments(
    project_id: int,
    request: Request,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    locale: str = Depends(get_locale)
):
    """Get comments for a project."""
    # Check if project exists
    project = project_repository.get(db, project_id)
    if not project:
        raise_not_found(locale, "project")

    comment_list = _build_comment_tree(db, project_id)
    if skip:
        comment_list = comment_list[skip:]
    if limit is not None:
        comment_list = comment_list[:limit]

    return {"comments": comment_list, "project_id": project_id}


@router.post("/{project_id}/comments", response_model=Comment)
async def create_project_comment(
    project_id: int,
    comment: CommentCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    locale: str = Depends(get_locale)
):
    """Create a comment on a project."""
    # Check if project exists
    project = project_repository.get(db, project_id)
    if not project:
        raise_not_found(locale, "project")

    # Create comment data with user ID
    comment_data = comment.model_dump()
    comment_data["user_id"] = current_user.id
    comment_data["project_id"] = project_id

    if comment.parent_id is not None:
        parent_comment = comment_repository.get(db, comment.parent_id)
        if not parent_comment:
            raise_not_found(locale, "comment")
        if parent_comment.project_id != project_id:
            raise_bad_request(locale, "Reply comment must belong to the same project")

    # Create the comment
    new_comment = comment_repository.create(db, obj_in=comment_data)
    db.refresh(new_comment)

    comment_with_relations = comment_repository.get(db, new_comment.id)
    return _serialize_comment(comment_with_relations or new_comment)
