import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from backend.database.session import Base


class PlayerProfile(Base):
    __tablename__ = "player_profiles"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    display_name = Column(String(50), nullable=False)
    avatar_url = Column(String(255), default="/assets/avatars/default_racer.png")
    country_code = Column(String(3), default="GLOBAL")
    
    level = Column(Integer, default=1, nullable=False)
    xp = Column(Integer, default=0, nullable=False)
    driver_rating = Column(Integer, default=1200, nullable=False)
    tier = Column(String(20), default="Bronze", nullable=False)
    tier_division = Column(Integer, default=1, nullable=False)
    
    total_races = Column(Integer, default=0, nullable=False)
    total_wins = Column(Integer, default=0, nullable=False)
    podium_finishes = Column(Integer, default=0, nullable=False)
    total_distance_km = Column(Float, default=0.0, nullable=False)
    total_drift_distance_meters = Column(Float, default=0.0, nullable=False)
    best_lap_time_ms = Column(Integer, default=0, nullable=False)
    clean_races_count = Column(Integer, default=0, nullable=False)
    
    favorite_vehicle_id = Column(String(50), nullable=True)
    favorite_track_id = Column(String(50), nullable=True)
    active_title = Column(String(50), default="Rookie Driver")
    unlocked_badges = Column(JSON, default=list)
    career_chapter_progress = Column(Integer, default=1)
    
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="profile")
