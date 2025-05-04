import uuid
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from database.database import Base

class Media(Base):
    __tablename__ = "media"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    media_type = Column(String, index=True, nullable=False)  # 'pdf' or 'video'
    category = Column(String, index=True, nullable=False)     # e.g., 'meditation', 'self-help'
    title = Column(String(255), index=True, nullable=False)
    url = Column(String, nullable=False)
