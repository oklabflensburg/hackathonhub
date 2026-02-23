"""
Comment API routes.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.auth import get_current_user
from app.domain.schemas.project import Comment, CommentCreate
from app.repositories.project_repository import CommentRepository

router = APIRouter()

# Initialize repository instance
comment_repository = CommentRepository()


@router.put("/{comment_id}", response_model=Comment)
async def update_comment(
    comment_id: int,
    comment_update: CommentCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Update a comment."""
    # Check if comment exists
    comment = comment_repository.get(db, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    # Check if user owns the comment
    if comment.user_id != current_user.id:
        raise HTTPException(
            status_code=403, 
            detail="Not authorized to update this comment"
        )
    
    # Update the comment
    update_data = comment_update.model_dump(exclude_unset=True)
    updated_comment = comment_repository.update(db, db_obj=comment, obj_in=update_data)
    
    return Comment.from_orm(updated_comment)


@router.delete("/{comment_id}")
async def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Delete a comment."""
    # Check if comment exists
    comment = comment_repository.get(db, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    # Check if user owns the comment or is admin
    if comment.user_id != current_user.id:
        # In a real implementation, check if user is admin
        # For now, only owner can delete
        raise HTTPException(
            status_code=403, 
            detail="Not authorized to delete this comment"
        )
    
    # Delete the comment
    comment_repository.delete(db, id=comment_id)
    
    return {"message": "Comment deleted successfully"}


@router.post("/{comment_id}/vote")
async def vote_for_comment(
    comment_id: int,
    vote_type: str,  # "upvote" or "downvote"
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
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
        raise HTTPException(
            status_code=400,
            detail="Vote type must be 'upvote' or 'downvote'"
        )
    
    # Check if comment exists
    comment = comment_repository.get(db, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    # Note: Comment voting implementation would need a CommentVote repository
    # For now, return a placeholder response
    raise HTTPException(
        status_code=501,
        detail="Comment voting not yet implemented"
    )


@router.delete("/{comment_id}/vote")
async def remove_comment_vote(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Remove vote from a comment."""
    # Check if comment exists
    comment = comment_repository.get(db, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    # Note: Comment voting implementation would need a CommentVote repository
    # For now, return a placeholder response
    raise HTTPException(
        status_code=501,
        detail="Comment voting not yet implemented"
    )