import uuid
from sqlalchemy import Column, String, Boolean
from sqlalchemy.dialects.postgresql import UUID  # If using PostgreSQL
from database.database import Base
from sqlalchemy.orm import relationship
from models.mood_model import Mood
from models.routine_model import Routine
from models.conversation_model import Conversation,Message,conversation_users

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    guardianEmail = Column(String, unique=True, index=True)
    guardianPhone = Column(String(15), unique=True, index=True)
    is_verified = Column(Boolean, index=True)
    verification_otp = Column(String(6))
    hashed_password = Column(String)
    is_admin = Column(Boolean, default=False, index=True)

    routines = relationship("Routine", back_populates="user")
    moods = relationship("Mood", back_populates="user")
    conversations = relationship("Conversation", secondary=conversation_users, back_populates="users")
    messages_sent = relationship("Message", back_populates="sender")



