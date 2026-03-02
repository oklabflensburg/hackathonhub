"""
CommentVote Repository.

This repository handles all database operations for CommentVote entities.
"""
from typing import Optional, List
from sqlalchemy.orm import Session

from app.domain.models import CommentVote
from app.repositories.base import BaseRepository


class CommentVoteRepository(BaseRepository[CommentVote]):
    """
    Repository for CommentVote operations.
    """

    def __init__(self):
        super().__init__(CommentVote)

    def get_by_user_and_comment(
        self, db: Session, user_id: int, comment_id: int
    ) -> Optional[CommentVote]:
        """
        Get a user's vote for a specific comment.

        Args:
            db: Database session
            user_id: User ID
            comment_id: Comment ID

        Returns:
            CommentVote if found, None otherwise
        """
        return db.query(self.model).filter(
            self.model.user_id == user_id,
            self.model.comment_id == comment_id
        ).first()

    def get_by_comment(self, db: Session,
                       comment_id: int) -> List[CommentVote]:
        """
        Get all votes for a comment.

        Args:
            db: Database session
            comment_id: Comment ID

        Returns:
            List of votes for the comment
        """
        return db.query(self.model).filter(
            self.model.comment_id == comment_id
        ).all()

    def get_by_user(self, db: Session,
                    user_id: int) -> List[CommentVote]:
        """
        Get all comment votes by a user.

        Args:
            db: Database session
            user_id: User ID

        Returns:
            List of comment votes by the user
        """
        return db.query(self.model).filter(
            self.model.user_id == user_id
        ).all()

    def create_vote(self, db: Session,
                    user_id: int,
                    comment_id: int,
                    vote_type: str = "upvote") -> CommentVote:
        """
        Create a new comment vote.

        Args:
            db: Database session
            user_id: User ID
            comment_id: Comment ID
            vote_type: Type of vote ("upvote" or "downvote")

        Returns:
            Created CommentVote
        """
        vote = CommentVote(
            user_id=user_id,
            comment_id=comment_id,
            vote_type=vote_type
        )

        db.add(vote)
        db.commit()
        db.refresh(vote)
        return vote

    def delete_by_user_and_comment(
        self, db: Session, user_id: int, comment_id: int
    ) -> bool:
        """
        Delete a user's vote for a comment.

        Args:
            db: Database session
            user_id: User ID
            comment_id: Comment ID

        Returns:
            True if vote was found and deleted, False otherwise
        """
        vote = self.get_by_user_and_comment(db, user_id, comment_id)
        if not vote:
            return False

        db.delete(vote)
        db.commit()
        return True

    def update_vote(
        self, db: Session, user_id: int, comment_id: int, vote_type: str
    ) -> Optional[CommentVote]:
        """
        Update an existing vote or create if not exists.

        Args:
            db: Database session
            user_id: User ID
            comment_id: Comment ID
            vote_type: New vote type

        Returns:
            Updated CommentVote or None if not found
        """
        vote = self.get_by_user_and_comment(db, user_id, comment_id)
        if not vote:
            return None

        vote.vote_type = vote_type
        db.commit()
        db.refresh(vote)
        return vote
