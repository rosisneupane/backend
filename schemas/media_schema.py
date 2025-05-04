# schemas.py or wherever your Pydantic models are

from pydantic import BaseModel
from uuid import UUID

class MediaOut(BaseModel):
    id: UUID
    media_type: str
    category: str
    title: str
    url: str

    class Config:
        orm_mode = True
