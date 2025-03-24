import uuid
from sqlalchemy import Column, String, Boolean, Date, Time, ForeignKey
from sqlalchemy.dialects.postgresql import UUID  # If using PostgreSQL
from database.database import Base
from sqlalchemy.orm import relationship

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

    routines = relationship("Routine", back_populates="user")
    moods = relationship("Mood", back_populates="user")


class Routine(Base):
    __tablename__ = "routines"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)
    text = Column(String, nullable=False)
    status = Column(Boolean, default=False)  # False for incomplete, True for complete

    user = relationship("User", back_populates="routines")
