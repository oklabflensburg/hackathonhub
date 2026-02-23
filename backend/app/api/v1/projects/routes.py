"""
Project API routes.
"""
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.auth import get_current_user
from app.domain.schemas.project import (
    Project, ProjectCreate, ProjectUpdate, CommentCreate, Comment
)
from app.services.project_service import project_service
from app.repositories.project_repository import ProjectRepository
from app.repositories.project_repository import VoteRepository
from app.repositories.project_repository import CommentRepository

router = APIRouter()

# Initialize repository instances
project_repository = ProjectRepository()
vote_repository = VoteRepository()
comment_repository = CommentRepository()


@router.get("/", response_model=List[Project])
async def get_projects(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all projects."""
    projects = project_service.get_projects(db, skip=skip, limit=limit)
    return projects


@router.get("/{project_id}", response_model=Project)
async def get_project(
    project_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific project by ID."""
    project = project_service.get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.post("/", response_model=Project)
async def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Create a new project."""
    new_project = project_service.create_project(
        db, project, current_user.id
    )
    return new_project


@router.put("/{project_id}", response_model=Project)
async def update_project(
    project_id: int,
    project_update: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Update a project."""
    # Note: The service should handle permission checking
    # For now, we'll check ownership here
    project = project_service.get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Check ownership (simplified - should be in service)
    # TODO: Move permission logic to service layer
    from app.repositories.project_repository import ProjectRepository
    project_repo = ProjectRepository()
    db_project = project_repo.get(db, project_id)
    if db_project.created_by != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized to update this project"
        )

    updated_project = project_service.update_project(
        db, project_id, project_update
    )
    if not updated_project:
        raise HTTPException(
            status_code=404, detail="Project not found or update failed"
        )
    return updated_project


@router.delete("/{project_id}")
async def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Delete a project."""
    # Check ownership first
    from app.repositories.project_repository import ProjectRepository
    project_repo = ProjectRepository()
    project = project_repo.get(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if project.created_by != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized to delete this project"
        )

    success = project_service.delete_project(db, project_id)
    if not success:
        raise HTTPException(
            status_code=500, detail="Failed to delete project"
        )

    return {"message": "Project deleted successfully"}


@router.post("/{project_id}/vote")
async def vote_for_project(
    project_id: int,
    vote_type: str = Body(..., embed=True),  # "upvote" or "downvote" from JSON body
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Vote for a project."""
    # Normalize vote type
    vote_type = vote_type.lower().strip()
    
    # Map 'up'/'down' to 'upvote'/'downvote' for compatibility
    if vote_type == 'up':
        vote_type = 'upvote'
    elif vote_type == 'down':
        vote_type = 'downvote'
    
    # Validate vote type
    if vote_type not in ["upvote", "downvote"]:
        raise HTTPException(
            status_code=400,
            detail="Vote type must be 'upvote' or 'downvote'"
        )

    # Check if project exists
    project = project_repository.get(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Check if user already voted
    existing_vote = vote_repository.get_user_vote_for_project(
        db, current_user.id, project_id
    )

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
            message = f"Changed vote to {vote_type}"
    else:
        # Create new vote
        vote_repository.create(db, obj_in={
            "user_id": current_user.id,
            "project_id": project_id,
            "vote_type": vote_type
        })
        message = f"Added {vote_type}"

    # Update vote counts
    vote_repository.update_vote_counts(db, project_id)

    return {
        "message": message,
        "project_id": project_id,
        "vote_type": vote_type
    }


@router.get("/{project_id}/vote-stats")
async def get_project_vote_stats(
    project_id: int,
    db: Session = Depends(get_db)
):
    """Get vote statistics for a project (public endpoint)."""
    # Check if project exists
    project = project_repository.get(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

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
    db: Session = Depends(get_db)
):
    """Increment view count for a project"""
    # Check if project exists
    project = project_repository.get(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Increment view count
    project.view_count = (project.view_count or 0) + 1
    db.commit()
    db.refresh(project)
    
    return {
        "message": "View count incremented",
        "view_count": project.view_count
    }


@router.delete("/{project_id}/vote")
async def remove_vote(
    project_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Remove user's vote from a project."""
    # Check if project exists
    project = project_repository.get(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Check if user has voted
    existing_vote = vote_repository.get_user_vote_for_project(
        db, current_user.id, project_id
    )
    if not existing_vote:
        raise HTTPException(status_code=404, detail="Vote not found")

    # Delete the vote
    vote_repository.delete(db, id=existing_vote.id)
    
    # Update vote counts
    vote_repository.update_vote_counts(db, project_id)
    
    # Get updated project stats
    project = project_repository.get(db, project_id)
    db.refresh(project)  # Ensure we have latest values

    return {
        "message": "Vote removed successfully",
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
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get comments for a project."""
    # Check if project exists
    project = project_repository.get(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Get comments
    comments = comment_repository.get_project_comments(
        db, project_id, skip=skip, limit=limit
    )

    # Convert to list of dicts with user info
    comment_list = []
    for comment in comments:
        # Get user info (simplified - would need user repository)
        from app.domain.models.user import User
        user = db.query(User).filter(User.id == comment.user_id).first()

        comment_list.append({
            "id": comment.id,
            "content": comment.content,
            "user_id": comment.user_id,
            "user_name": user.username if user else "Unknown",
            "upvote_count": comment.upvote_count,
            "downvote_count": comment.downvote_count,
            "vote_score": comment.vote_score,
            "created_at": comment.created_at,
            "replies": comment_repository.get_replies(db, comment.id)
        })

    return {"comments": comment_list, "project_id": project_id}


@router.post("/{project_id}/comments", response_model=Comment)
async def create_project_comment(
    project_id: int,
    comment: CommentCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Create a comment on a project."""
    # Check if project exists
    project = project_repository.get(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Create comment data with user ID
    comment_data = comment.model_dump()
    comment_data["user_id"] = current_user.id
    comment_data["project_id"] = project_id
    
    # Create the comment
    new_comment = comment_repository.create(db, obj_in=comment_data)
    
    return Comment.from_orm(new_comment)
