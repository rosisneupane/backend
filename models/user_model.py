from sqlalchemy import Column, Integer, String,Boolean
from database.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    guardianEmail=Column(String, unique=True, index=True)
    guardianPhone = Column(String(15), unique=True, index=True)
    is_verified = Column(Boolean, index=True)
    verification_otp = Column(String(6))
    hashed_password = Column(String)
