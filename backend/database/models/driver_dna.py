import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from backend.database.session import Base


class DriverDNA(Base):
    __tablename__ = "driver_dna"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    
    aggression = Column(Float, default=0.50, nullable=False)
    cornering = Column(Float, default=0.50, nullable=False)
    overtaking = Column(Float, default=0.50, nullable=False)
    drifting = Column(Float, default=0.50, nullable=False)
    consistency = Column(Float, default=0.50, nullable=False)
    wet_racing = Column(Float, default=0.50, nullable=False)
    risk_management = Column(Float, default=0.50, nullable=False)
    
    driving_archetype = Column(String(50), default="Balanced Prodigy")
    cluster_id = Column(String(20), default="C_BALANCED")
    sample_races_count = Column(Float, default=0.0)
    raw_telemetry_metrics = Column(JSON, default=dict)
    
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="driver_dna")
