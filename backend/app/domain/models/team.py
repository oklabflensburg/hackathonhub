"""
Team domain models.
"""
from sqlalchemy import (
    Column, Integer, String, Text, DateTime,
    ForeignKey, Boolean, UniqueConstraint
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .base import Base


class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    hackathon_id = Column(Integer, ForeignKey("hackathons.id"), nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    max_members = Column(Integer, default=5)
    is_open = Column(Boolean, default=True)  # Open for new members

    # Relationships will be defined in __init__.py
    # hackathon = relationship("Hackathon", back_populates="teams")
    # creator = relationship("User", foreign_keys=[created_by])
    # members = relationship("TeamMember", back_populates="team")
    # invitations = relationship("TeamInvitation", back_populates="team")
    # projects = relationship("Project", back_populates="team")


class TeamMember(Base):
    __tablename__ = "team_members"

    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    role = Column(String(20), default='member')  # 'owner' or 'member'
    joined_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        UniqueConstraint(
            'team_id', 'user_id',
            name='_team_user_member_uc'
        ),
    )

    # Relationships will be defined in __init__.py
    # team = relationship("Team", back_populates="members")
    # user = relationship("User", back_populates="team_memberships")


class TeamInvitation(Base):
    __tablename__ = "team_invitations"

    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    invited_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    invited_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    # 'pending', 'accepted', 'declined'
    status = Column(String(20), default='pending')
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True))

    __table_args__ = (
        UniqueConstraint(
            'team_id', 'invited_user_id',
            name='_team_user_invitation_uc'
        ),
    )

    # Relationships will be defined in __init__.py
    # team = relationship("Team", back_populates="invitations")
    # invited_user = relationship(
    #     "User",
    #     foreign_keys=[invited_user_id],
    #     back_populates="team_invitations"
    # )
    # inviter = relationship(
    #     "User",
    #     foreign_keys=[invited_by],
    #     back_populates="team_invitations_sent"
    # )