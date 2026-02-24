"""
Comment API routes.
"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.auth import get_current_user
from app.domain.schemas.project import Comment, CommentCreate
from app.repositories.project_repository import CommentRepository
from app.i18n.dependencies import get_locale
from app.i18n.helpers import (
    raise_not_found,
    raise_forbidden,
    raise_bad_request,
    raise_i18n_http_exception
)

router = APIRouter()

# Initialize repository instance
comment_repository = CommentRepository()


@router.put("/{comment_id}", response_model=Comment)
async def update_comment(
    comment_id: int,
    comment_update: CommentCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    locale: str = Depends(get_locale)
):
    """Update a comment."""
    # Check if comment exists
    comment = comment_repository.get(db, comment_id)
    if not comment:
        raise_not_found(locale, "comment")
    
    # Check if user owns the comment
    if comment.user_id != current_user.id:
        raise_forbidden(locale, "update", entity="comment")
    
    # Update the comment
    update_data = comment_update.model_dump(exclude_unset=True)
    updated_comment = comment_repository.update(
        db, db_obj=comment, obj_in=update_data
    )
    
    return Comment.from_orm(updated_comment)


@router.delete("/{comment_id}")
async def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    locale: str = Depends(get_locale)
):
    """Delete a comment."""
    # Check if comment exists
    comment = comment_repository.get(db, comment_id)
    if not comment:
        raise_not_found(locale, "comment")
    
    # Check if user owns the comment or is admin
    if comment.user_id != current_user.id:
        # In a real implementation, check if user is admin
        # For now, only owner can delete
        raise_forbidden(locale, "delete", entity="comment")
    
    # Delete the comment
    comment_repository.delete(db, id=comment_id)
    
    return {"message": "Comment deleted successfully"}


@router.post("/{comment_id}/vote")
async def vote_for_comment(
    comment_id: int,
    vote_type: str,  # "upvote" or "downvote"
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    locale: str = Depends(get_locale)
):
    """Vote for a comment."""
    # Normalize vote type
    vote_type = vote_type.lower().strip()
    
    # Map 'up'/'down' to 'upvote'/'downvote' for compatibility
    if vote_type == 'up':
        vote_type = 'upvote'
    elif vote_type == 'down':
        vote_type = 'downvote'
    
    # Validate vote type
    if vote_type not in ["upvote", "downvote"]:
        raise_bad_request(locale, "vote_type_invalid")
    
    # Check if comment exists
    comment = comment_repository.get(db, comment_id)
    if not comment:
        raise_not_found(locale, "comment")
    
    # Note: Comment voting implementation would need a CommentVote repository
    # For now, return a placeholder response
    raise_i18n_http_exception(
        locale=locale,
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        translation_key="errors.comment_voting_not_implemented"
    )


@router.delete("/{comment_id}/vote")
async def remove_comment_vote(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    locale: str = Depends(get_locale)
):
    """Remove vote from a comment."""
    # Check if comment exists
    comment = comment_repository.get(db, comment_id)
    if not comment:
        raise_not_found(locale, "comment")
    
    # Note: Comment voting implementation would need a CommentVote repository
    # For now, return a placeholder response
    raise_i18n_http_exception(
        locale=locale,
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        translation_key="errors.comment_voting_not_implemented"
    )