import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, ForeignKey, DateTime, JSON
from backend.database.session import Base


class AntiCheatLog(Base):
    __tablename__ = "anti_cheat_logs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    race_id = Column(String(36), nullable=True, index=True)
    violation_type = Column(String(50), nullable=False)
    severity = Column(String(20), default="HIGH")  # LOW, MEDIUM, HIGH, CRITICAL
    confidence_score = Column(Float, default=1.0)
    telemetry_snapshot = Column(JSON, default=dict)
    action_taken = Column(String(50), default="FLAGGED_FOR_REVIEW")
    created_at = Column(DateTime, default=datetime.utcnow)
