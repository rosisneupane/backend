import uuid
from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from database.database import Base



class Collection(Base):
    __tablename__ = 'collections'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    videos = relationship("Video", back_populates="collection", cascade="all, delete")

class Video(Base):
    __tablename__ = 'videos'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    title = Column(String, nullable=False)
    url = Column(String, nullable=False)
    collection_id = Column(UUID(as_uuid=True), ForeignKey('collections.id', ondelete="CASCADE"))
    collection = relationship("Collection", back_populates="videos")
