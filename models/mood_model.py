import uuid
from sqlalchemy import Column, String, Boolean, Date, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID  # If using PostgreSQL
from database.database import Base
from sqlalchemy.orm import relationship

class Mood(Base):
    __tablename__ = "moods"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    date = Column(Date, nullable=False)
    mood_rating = Column(Integer, nullable=False)  # Mood rating from 1 to 5

    # Relationship with User
    user = relationship("User", back_populates="moods")
