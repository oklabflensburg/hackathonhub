"""
Vote Repository.

This repository handles all database operations for Vote entities.
"""
from typing import Optional, List
from sqlalchemy.orm import Session

from app.domain.models import Vote
from app.repositories.base import BaseRepository


class VoteRepository(BaseRepository[Vote]):
    """
    Repository for Vote operations.
    """

    def __init__(self):
        super().__init__(Vote)

    def get_by_user_and_project(
        self, db: Session, user_id: int, project_id: int
    ) -> Optional[Vote]:
        """
        Get a user's vote for a specific project.

        Args:
            db: Database session
            user_id: User ID
            project_id: Project ID

        Returns:
            Vote if found, None otherwise
        """
        return db.query(self.model).filter(
            self.model.user_id == user_id,
            self.model.project_id == project_id
        ).first()

    def get_by_project(self, db: Session,
                       project_id: int) -> List[Vote]:
        """
        Get all votes for a project.

        Args:
            db: Database session
            project_id: Project ID

        Returns:
            List of votes for the project
        """
        return db.query(self.model).filter(
            self.model.project_id == project_id
        ).all()

    def get_by_user(self, db: Session,
                    user_id: int) -> List[Vote]:
        """
        Get all votes by a user.

        Args:
            db: Database session
            user_id: User ID

        Returns:
            List of votes by the user
        """
        return db.query(self.model).filter(
            self.model.user_id == user_id
        ).all()

    def create_vote(self, db: Session,
                    user_id: int,
                    project_id: int,
                    vote_type: str = "upvote") -> Vote:
        """
        Create a new vote.

        Args:
            db: Database session
            user_id: User ID
            project_id: Project ID
            vote_type: Type of vote ("upvote" or "downvote")

        Returns:
            Created Vote
        """
        vote = Vote(
            user_id=user_id,
            project_id=project_id,
            vote_type=vote_type
        )

        db.add(vote)
        db.commit()
        db.refresh(vote)
        return vote

    def delete_by_user_and_project(self, db: Session,
                                   user_id: int,
                                   project_id: int) -> bool:
        """
        Delete a user's vote for a project.

        Args:
            db: Database session
            user_id: User ID
            project_id: Project ID

        Returns:
            True if vote was found and deleted, False otherwise
        """
        vote = self.get_by_user_and_project(db, user_id, project_id)
        if not vote:
            return False

        db.delete(vote)
        db.commit()
        return True
