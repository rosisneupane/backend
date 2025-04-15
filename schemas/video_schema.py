# schemas.py
from uuid import UUID
from pydantic import BaseModel
from typing import Optional, List

class VideoBase(BaseModel):
    title: str
    url: str

class VideoCreate(VideoBase):
    pass

class VideoUpdate(VideoBase):
    pass

class VideoMain(VideoBase):
    id: UUID
    collection_id: UUID

    class Config:
        orm_mode = True

class CollectionBase(BaseModel):
    name: str
    description: Optional[str] = None

class CollectionCreate(CollectionBase):
    pass

class CollectionUpdate(CollectionBase):
    pass

class CollectionMain(CollectionBase):
    id: UUID
    videos: List[VideoMain] = []

    class Config:
        orm_mode = True
