from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
import uuid
from sqlalchemy.dialects.postgresql import UUID  # If using PostgreSQL
from datetime import datetime
from database.database import Base  # Adjust import path if needed

class EmergencyAlert(Base):
    __tablename__ = "emergency_alerts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    conversation_id = Column(UUID(as_uuid=True), ForeignKey("ai_conversations.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    message = Column(String, nullable=False)

    conversation = relationship("AiConversation", back_populates="emergency_alerts")
    user = relationship("User", back_populates="emergency_alerts")
