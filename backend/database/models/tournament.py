import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, JSON, Boolean
from backend.database.session import Base


class Tournament(Base):
    __tablename__ = "tournaments"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(100), nullable=False)
    description = Column(String(255), nullable=False)
    format = Column(String(30), default="Knockout")  # Knockout, RoundRobin, Swiss, TimeTrial
    entry_fee_tickets = Column(Integer, default=2)
    prize_pool_credits = Column(Integer, default=100000)
    prize_pool_gold = Column(Integer, default=500)
    min_rank_tier = Column(String(20), default="Bronze")
    max_participants = Column(Integer, default=64)
    bracket_data = Column(JSON, default=dict)
    is_active = Column(Boolean, default=True)
    starts_at = Column(DateTime, nullable=False)
    ends_at = Column(DateTime, nullable=False)
