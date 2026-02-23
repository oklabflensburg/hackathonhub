"""
Project domain models including Project, Vote, Comment, and CommentVote.
"""
from sqlalchemy import (
    Column, Integer, String, Text, DateTime,
    ForeignKey, Boolean, UniqueConstraint
)
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql import func

from .base import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    repository_url = Column(String)
    live_url = Column(String)
    technologies = Column(String)  # Comma-separated list
    status = Column(String, default="active")  # active, completed, archived
    is_public = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    owner_id = Column(Integer, ForeignKey("users.id"))
    image_path = Column(String)  # Path to uploaded image file
    upvote_count = Column(Integer, default=0)
    downvote_count = Column(Integer, default=0)
    vote_score = Column(Integer, default=0)  # upvotes - downvotes
    comment_count = Column(Integer, default=0)
    view_count = Column(Integer, default=0)  # Project view count
    hackathon_id = Column(Integer, ForeignKey("hackathons.id"), nullable=True)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=True)

    # Relationships will be defined in __init__.py
    # owner = relationship("User", back_populates="projects")
    # hackathon = relationship("Hackathon", back_populates="projects")
    # team = relationship("Team")
    # votes = relationship("Vote", back_populates="project")
    # comments = relationship("Comment", back_populates="project")


class Vote(Base):
    __tablename__ = "votes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    project_id = Column(Integer, ForeignKey("projects.id"))
    vote_type = Column(String, nullable=False)  # 'upvote' or 'downvote'
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        UniqueConstraint(
            'user_id', 'project_id',
            name='_user_project_vote_uc'
        ),
    )

    # Relationships will be defined in __init__.py
    # user = relationship("User", back_populates="votes")
    # project = relationship("Project", back_populates="votes")


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    project_id = Column(Integer, ForeignKey("projects.id"))
    parent_id = Column('parent_comment_id', Integer,
                       ForeignKey("comments.id"), nullable=True)
    upvote_count = Column(Integer, default=0)
    downvote_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    @hybrid_property
    def vote_score(self):
        return self.upvote_count - self.downvote_count

    # Relationships will be defined in __init__.py
    # user = relationship("User", back_populates="comments")
    # project = relationship("Project", back_populates="comments")
    # parent = relationship(
    #     "Comment",
    #     remote_side=[id],
    #     back_populates="replies"
    # )
    # replies = relationship(
    #     "Comment",
    #     back_populates="parent",
    #     cascade="all, delete-orphan"
    # )
    # votes = relationship("CommentVote", back_populates="comment")


class CommentVote(Base):
    __tablename__ = "comment_votes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    comment_id = Column(Integer, ForeignKey("comments.id"))
    vote_type = Column(String, nullable=False)  # 'upvote' or 'downvote'
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        UniqueConstraint(
            'user_id', 'comment_id',
            name='_user_comment_vote_uc'
        ),
    )

    # Relationships will be defined in __init__.py
    # user = relationship("User", back_populates="comment_votes")
    # comment = relationship("Comment", back_populates="votes")