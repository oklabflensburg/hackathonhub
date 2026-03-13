"""
Comment API routes.
"""
from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.core.database import get_db
from app.core.auth import get_current_user
from app.core.permissions import can_manage_comment
from app.domain.schemas.project import Comment, CommentCreate
from app.domain.models import CommentVote
from app.repositories.project_repository import CommentRepository
from app.repositories.comment_vote_repository import CommentVoteRepository
from app.i18n.dependencies import get_locale
from app.i18n.helpers import (
    raise_not_found,
    raise_forbidden,
    raise_bad_request
)

router = APIRouter()

# Initialize repository instances
comment_repository = CommentRepository()
comment_vote_repository = CommentVoteRepository()


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

    if not can_manage_comment(db, current_user, comment):
        raise_forbidden(locale, "update", entity="comment")

    # Update the comment
    update_data = comment_update.model_dump(exclude_unset=True)
    updated_comment = comment_repository.update(
        db, db_obj=comment, obj_in=update_data
    )

    return Comment.model_validate(updated_comment)


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

    if not can_manage_comment(db, current_user, comment):
        raise_forbidden(locale, "delete", entity="comment")

    # Delete the comment
    comment_repository.delete(db, id=comment_id)

    return {"message": "Comment deleted successfully"}


@router.post("/{comment_id}/vote")
async def vote_for_comment(
    comment_id: int,
    # "upvote" or "downvote" from JSON body
    vote_type: str = Body(..., embed=True),
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

    try:
        # Check if user already voted
        existing_vote = comment_vote_repository.get_by_user_and_comment(
            db, current_user.id, comment_id
        )

        vote_obj = None
        message = ""

        if existing_vote:
            # Update existing vote
            if existing_vote.vote_type == vote_type:
                # Same vote type - remove the vote
                comment_vote_repository.delete_by_user_and_comment(
                    db, current_user.id, comment_id
                )
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
                vote_obj = comment_vote_repository.create_vote(
                    db, current_user.id, comment_id, vote_type
                )
                message = f"Added {vote_type}"
            except IntegrityError:
                # Race condition: vote was created by another request
                db.rollback()

                # Get the current vote state
                existing_vote = comment_vote_repository.get_by_user_and_comment(
                    db, current_user.id, comment_id
                )
                if existing_vote:
                    # Another request created a vote, return current state
                    message = f"Already voted {existing_vote.vote_type}"
                    vote_type = existing_vote.vote_type
                    vote_obj = existing_vote
                else:
                    # Retry once (should rarely happen)
                    vote_obj = comment_vote_repository.create_vote(
                        db, current_user.id, comment_id, vote_type
                    )
                    message = f"Added {vote_type}"

    except IntegrityError:
        db.rollback()
        raise_bad_request(locale, "vote_conflict")

    # Update comment vote counts
    # Calculate upvote/downvote counts from database
    upvotes = db.query(CommentVote).filter(
        CommentVote.comment_id == comment_id,
        CommentVote.vote_type == "upvote"
    ).count()
    downvotes = db.query(CommentVote).filter(
        CommentVote.comment_id == comment_id,
        CommentVote.vote_type == "downvote"
    ).count()

    comment.upvote_count = upvotes
    comment.downvote_count = downvotes
    db.commit()
    db.refresh(comment)

    response_data = {
        "message": message,
        "comment_id": comment_id,
        "vote_type": vote_type,
        "comment_stats": {
            "comment_id": comment_id,
            "upvotes": comment.upvote_count,
            "downvotes": comment.downvote_count,
            "total_score": comment.vote_score,
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
            "comment_id": vote_obj.comment_id,
            "vote_type": vote_obj.vote_type,
            "created_at": (
                vote_obj.created_at.isoformat()
                if vote_obj.created_at
                else None
            )
        }

    return response_data


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

    # Check if user has voted
    existing_vote = comment_vote_repository.get_by_user_and_comment(
        db, current_user.id, comment_id
    )
    if not existing_vote:
        raise_bad_request(locale, "no_vote_to_remove")

    # Delete the vote
    comment_vote_repository.delete_by_user_and_comment(
        db, current_user.id, comment_id
    )

    # Update comment vote counts
    upvotes = db.query(CommentVote).filter(
        CommentVote.comment_id == comment_id,
        CommentVote.vote_type == "upvote"
    ).count()
    downvotes = db.query(CommentVote).filter(
        CommentVote.comment_id == comment_id,
        CommentVote.vote_type == "downvote"
    ).count()

    comment.upvote_count = upvotes
    comment.downvote_count = downvotes
    db.commit()
    db.refresh(comment)

    return {
        "message": "Vote removed",
        "comment_id": comment_id,
        "comment_stats": {
            "comment_id": comment_id,
            "upvotes": comment.upvote_count,
            "downvotes": comment.downvote_count,
            "total_score": comment.vote_score,
            "user_vote": None
        }
    }
