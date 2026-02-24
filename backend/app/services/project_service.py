"""
Project service layer for business logic operations.
"""
from typing import Optional, List
from sqlalchemy.orm import Session

from app.domain.schemas.project import (
    ProjectCreate, ProjectUpdate, Project as ProjectSchema,
    Vote as VoteSchema, Comment as CommentSchema, CommentCreate
)
from app.repositories.project_repository import (
    ProjectRepository, VoteRepository, CommentRepository
)
from app.repositories.user_repository import UserRepository


class ProjectService:
    """Service for project-related business logic."""

    def __init__(self):
        self.project_repo = ProjectRepository()
        self.vote_repo = VoteRepository()
        self.comment_repo = CommentRepository()
        self.user_repo = UserRepository()

    def get_projects(
        self, db: Session, skip: int = 0, limit: int = 100
    ) -> List[ProjectSchema]:
        """Get all public projects."""
        projects = self.project_repo.get_public_projects(
            db, skip=skip, limit=limit
        )
        return [ProjectSchema.model_validate(p) for p in projects]

    def get_project(
        self, db: Session, project_id: int
    ) -> Optional[ProjectSchema]:
        """Get a project by ID and increment view count."""
        project = self.project_repo.get(db, project_id)
        if project:
            # Business logic: increment view count
            project.view_count = (project.view_count or 0) + 1
            db.commit()
            db.refresh(project)
            return ProjectSchema.model_validate(project)
        return None

    def create_project(
        self, db: Session, project_create: ProjectCreate, creator_id: int
    ) -> ProjectSchema:
        """Create a new project."""
        # Business logic: set creator and initial status
        project_data = project_create.model_dump()
        project_data["owner_id"] = creator_id
        project_data["status"] = "active"

        project = self.project_repo.create(db, obj_in=project_data)
        return ProjectSchema.model_validate(project)

    def update_project(
        self, db: Session, project_id: int, project_update: ProjectUpdate
    ) -> Optional[ProjectSchema]:
        """Update a project."""
        project = self.project_repo.get(db, project_id)
        if not project:
            return None

        update_data = project_update.model_dump(exclude_unset=True)
        updated_project = self.project_repo.update(
            db, db_obj=project, obj_in=update_data)
        return ProjectSchema.model_validate(updated_project)

    def delete_project(self, db: Session, project_id: int) -> bool:
        """Delete a project."""
        project = self.project_repo.get(db, project_id)
        if not project:
            return False

        self.project_repo.delete(db, id=project_id)
        return True

    def get_project_votes(
        self, db: Session, project_id: int
    ) -> List[VoteSchema]:
        """Get all votes for a project."""
        votes = self.vote_repo.get_by_project_id(db, project_id)
        return [VoteSchema.model_validate(v) for v in votes]

    def add_vote(
        self, db: Session, project_id: int, user_id: int,
        vote_type: str = "upvote"
    ) -> Optional[VoteSchema]:
        """Add a vote to a project."""
        # Map 'up'/'down' to 'upvote'/'downvote' for compatibility
        if vote_type == 'up':
            vote_type = 'upvote'
        elif vote_type == 'down':
            vote_type = 'downvote'

        # Validate vote type
        if vote_type not in ["upvote", "downvote"]:
            raise ValueError("Vote type must be 'upvote' or 'downvote'")

        # Business logic: check if user already voted
        existing_vote = self.vote_repo.get_by_user_and_project(
            db, user_id, project_id
        )
        if existing_vote:
            # Update existing vote
            existing_vote.vote_type = vote_type
            db.commit()
            db.refresh(existing_vote)
            return VoteSchema.model_validate(existing_vote)

        # Create new vote
        vote_data = {
            "project_id": project_id,
            "user_id": user_id,
            "vote_type": vote_type
        }
        vote = self.vote_repo.create(db, obj_in=vote_data)

        # Update project vote count
        project = self.project_repo.get(db, project_id)
        if project:
            if vote_type == "upvote":
                project.up_votes = (project.up_votes or 0) + 1
            else:
                project.down_votes = (project.down_votes or 0) + 1
            db.commit()

        return VoteSchema.model_validate(vote)

    def remove_vote(self, db: Session, project_id: int, user_id: int) -> bool:
        """Remove a user's vote from a project."""
        vote = self.vote_repo.get_by_user_and_project(db, user_id, project_id)
        if not vote:
            return False

        # Update project vote count
        project = self.project_repo.get(db, project_id)
        if project:
            if vote.vote_type == "upvote":
                project.up_votes = max(0, (project.up_votes or 0) - 1)
            else:
                project.down_votes = max(0, (project.down_votes or 0) - 1)
            db.commit()

        self.vote_repo.delete(db, id=vote.id)
        return True

    def get_project_comments(
        self, db: Session, project_id: int
    ) -> List[CommentSchema]:
        """Get all comments for a project."""
        comments = self.comment_repo.get_by_project_id(db, project_id)
        return [CommentSchema.model_validate(c) for c in comments]

    def add_comment(
        self, db: Session, project_id: int, user_id: int,
        comment_create: CommentCreate
    ) -> CommentSchema:
        """Add a comment to a project."""
        comment_data = comment_create.model_dump()
        comment_data["project_id"] = project_id
        comment_data["user_id"] = user_id

        comment = self.comment_repo.create(db, obj_in=comment_data)
        return CommentSchema.model_validate(comment)

    def delete_comment(
        self, db: Session, comment_id: int, user_id: int
    ) -> bool:
        """Delete a comment (only by owner or admin)."""
        comment = self.comment_repo.get(db, comment_id)
        if not comment:
            return False

        # Business logic: check permissions
        if comment.user_id != user_id:
            # Check if user is admin (simplified)
            user = self.user_repo.get(db, user_id)
            if not user or not user.is_admin:
                return False

        self.comment_repo.delete(db, id=comment_id)
        return True


# Global instance for dependency injection
project_service = ProjectService()
