"""
Project repository for database operations.
"""
from typing import List
from sqlalchemy.orm import Session

from app.repositories.base import BaseRepository
from app.domain.models.project import Project, Vote, Comment


class ProjectRepository(BaseRepository[Project]):
    """Repository for projects."""
    
    def __init__(self):
        super().__init__(Project)
    
    def get_public_projects(
        self, db: Session, skip: int = 0, limit: int = 100
    ) -> List[Project]:
        """Get public projects."""
        return db.query(self.model).filter(
            self.model.is_public.is_(True)
        ).order_by(
            self.model.created_at.desc()
        ).offset(skip).limit(limit).all()
    
    def get_by_owner(
        self, db: Session, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[Project]:
        """Get projects by owner."""
        return db.query(self.model).filter(
            self.model.owner_id == owner_id
        ).order_by(
            self.model.created_at.desc()
        ).offset(skip).limit(limit).all()
    
    def get_by_hackathon(
        self, db: Session, hackathon_id: int, skip: int = 0, limit: int = 100
    ) -> List[Project]:
        """Get projects by hackathon."""
        return db.query(self.model).filter(
            self.model.hackathon_id == hackathon_id
        ).order_by(
            self.model.created_at.desc()
        ).offset(skip).limit(limit).all()
    
    def get_by_team(
        self, db: Session, team_id: int, skip: int = 0, limit: int = 100
    ) -> List[Project]:
        """Get projects by team."""
        return db.query(self.model).filter(
            self.model.team_id == team_id
        ).order_by(
            self.model.created_at.desc()
        ).offset(skip).limit(limit).all()


class VoteRepository(BaseRepository[Vote]):
    """Repository for votes."""
    
    def __init__(self):
        super().__init__(Vote)
    
    def get_user_vote_for_project(
        self, db: Session, user_id: int, project_id: int
    ) -> Vote:
        """Get a user's vote for a project."""
        return db.query(self.model).filter(
            self.model.user_id == user_id,
            self.model.project_id == project_id
        ).first()
    
    def update_vote_counts(
        self, db: Session, project_id: int
    ) -> None:
        """Update vote counts for a project."""
        from sqlalchemy import func
        
        # Count upvotes and downvotes
        upvotes = db.query(func.count(self.model.id)).filter(
            self.model.project_id == project_id,
            self.model.vote_type == "upvote"
        ).scalar()
        
        downvotes = db.query(func.count(self.model.id)).filter(
            self.model.project_id == project_id,
            self.model.vote_type == "downvote"
        ).scalar()
        
        # Update project
        project = db.query(Project).filter(Project.id == project_id).first()
        if project:
            project.upvote_count = upvotes or 0
            project.downvote_count = downvotes or 0
            project.vote_score = (upvotes or 0) - (downvotes or 0)
            db.commit()


class CommentRepository(BaseRepository[Comment]):
    """Repository for comments."""
    
    def __init__(self):
        super().__init__(Comment)
    
    def get_project_comments(
        self, db: Session, project_id: int, skip: int = 0, limit: int = 100
    ) -> List[Comment]:
        """Get comments for a project."""
        return db.query(self.model).filter(
            self.model.project_id == project_id,
            self.model.parent_id.is_(None)  # Top-level comments only
        ).order_by(
            self.model.created_at.desc()
        ).offset(skip).limit(limit).all()
    
    def get_replies(
        self, db: Session, comment_id: int
    ) -> List[Comment]:
        """Get replies to a comment."""
        return db.query(self.model).filter(
            self.model.parent_id == comment_id
        ).order_by(
            self.model.created_at.asc()
        ).all()