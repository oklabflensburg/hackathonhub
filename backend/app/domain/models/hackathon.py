"""
Hackathon domain models.
"""
from sqlalchemy import (
    Column, Integer, String, Text, DateTime,
    ForeignKey, Boolean, Float, UniqueConstraint
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .base import Base


class Hackathon(Base):
    __tablename__ = "hackathons"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    start_date = Column(DateTime(timezone=True))
    end_date = Column(DateTime(timezone=True))
    location = Column(String)  # Physical or virtual
    latitude = Column(Float, nullable=True)  # Geographic coordinates
    longitude = Column(Float, nullable=True)
    website = Column(String)
    image_url = Column(String)  # URL to hackathon banner/image
    banner_path = Column(String)  # Path to uploaded banner file
    participant_count = Column(Integer, default=0)  # Registered participants
    view_count = Column(Integer, default=0)  # Page views
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    max_participants = Column(Integer, nullable=True)  # Optional limit
    registration_open = Column(Boolean, default=True)
    prizes = Column(Text, nullable=True)  # JSON or text description of prizes
    rules = Column(Text, nullable=True)  # Rules and guidelines
    organizers = Column(Text, nullable=True)  # JSON or text of organizers
    prize_pool = Column(String, nullable=True)  # Total prize amount
    owner_id = Column(Integer, ForeignKey("users.id"),
                      nullable=True)  # Creator

    # Relationships will be defined in __init__.py
    # registrations = relationship(
    #     "HackathonRegistration",
    #     back_populates="hackathon"
    # )
    # projects = relationship("Project", back_populates="hackathon")
    # teams = relationship("Team", back_populates="hackathon")
    # chat_rooms = relationship("ChatRoom", back_populates="hackathon")
    # owner = relationship("User")


class HackathonRegistration(Base):
    __tablename__ = "hackathon_registrations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    hackathon_id = Column(Integer, ForeignKey("hackathons.id"))
    registered_at = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String, default="registered")  # registered, attended

    # Unique constraint to prevent duplicate registrations
    __table_args__ = (
        UniqueConstraint(
            'user_id', 'hackathon_id',
            name='_user_hackathon_uc'
        ),
    )

    # Relationships will be defined in __init__.py
    # user = relationship("User")
    # hackathon = relationship("Hackathon")