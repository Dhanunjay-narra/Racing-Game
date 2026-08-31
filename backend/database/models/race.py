import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, Boolean, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from backend.database.session import Base


class RaceSessionModel(Base):
    __tablename__ = "race_sessions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    track_id = Column(String(50), nullable=False)
    race_mode = Column(String(30), default="Circuit")
    weather = Column(String(20), default="Clear")
    time_of_day = Column(String(20), default="Noon")
    total_laps = Column(Integer, default=3)
    max_players = Column(Integer, default=8)
    server_address = Column(String(100), default="127.0.0.1:8765")
    status = Column(String(20), default="CREATED")
    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime, nullable=True)
    ended_at = Column(DateTime, nullable=True)

    results = relationship("RaceResult", back_populates="race_session", cascade="all, delete-orphan")


class RaceResult(Base):
    __tablename__ = "race_results"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    race_session_id = Column(String(36), ForeignKey("race_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    vehicle_id = Column(String(50), nullable=False)
    
    position = Column(Integer, nullable=False)
    total_time_ms = Column(Integer, nullable=False)
    best_lap_time_ms = Column(Integer, nullable=False)
    top_speed_kmh = Column(Float, default=0.0)
    avg_speed_kmh = Column(Float, default=0.0)
    collisions_count = Column(Integer, default=0)
    drift_score = Column(Integer, default=0)
    clean_race = Column(Boolean, default=True)
    xp_earned = Column(Integer, default=0)
    credits_earned = Column(Integer, default=0)
    rating_delta = Column(Integer, default=0)
    validation_status = Column(String(20), default="VALID")
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="race_results")
    race_session = relationship("RaceSessionModel", back_populates="results")
