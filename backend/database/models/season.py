import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, JSON, Boolean
from backend.database.session import Base


class Season(Base):
    __tablename__ = "seasons"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    season_number = Column(Integer, unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    theme = Column(String(100), default="Apex Velocity")
    max_tier = Column(Integer, default=50)
    rewards_matrix = Column(JSON, default=dict)
    is_active = Column(Boolean, default=True)
    starts_at = Column(DateTime, nullable=False)
    ends_at = Column(DateTime, nullable=False)
