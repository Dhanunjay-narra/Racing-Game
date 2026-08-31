import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, JSON, Boolean
from sqlalchemy.orm import relationship
from backend.database.session import Base


class Club(Base):
    __tablename__ = "clubs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(50), unique=True, nullable=False, index=True)
    tag = Column(String(6), unique=True, nullable=False)
    description = Column(String(255), default="A competitive racing club.")
    badge_icon = Column(String(50), default="shield_flame")
    primary_color = Column(String(20), default="#FF3366")
    secondary_color = Column(String(20), default="#111111")
    
    owner_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    level = Column(Integer, default=1, nullable=False)
    xp = Column(Integer, default=0, nullable=False)
    trophies = Column(Integer, default=0, nullable=False)
    is_open = Column(Boolean, default=True)
    min_rating_required = Column(Integer, default=1000)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    members = relationship("ClubMember", back_populates="club", cascade="all, delete-orphan")


class ClubMember(Base):
    __tablename__ = "club_members"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    club_id = Column(String(36), ForeignKey("clubs.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    role = Column(String(20), default="member")  # owner, co_leader, veteran, member
    contributed_xp = Column(Integer, default=0)
    joined_at = Column(DateTime, default=datetime.utcnow)

    club = relationship("Club", back_populates="members")
