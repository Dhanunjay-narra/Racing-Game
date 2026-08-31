import uuid
from datetime import datetime
from sqlalchemy import Column, String, ForeignKey, DateTime, Boolean
from backend.database.session import Base


class FriendRelationship(Base):
    __tablename__ = "friends"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    friend_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    status = Column(String(20), default="ACCEPTED")  # PENDING, ACCEPTED, BLOCKED
    created_at = Column(DateTime, default=datetime.utcnow)
