from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class MessageCreate(BaseModel):
    conversation_id: UUID
    content: str

class UserBasic(BaseModel):
    id: UUID
    username: str
    email: str

    class Config:
        orm_mode = True

class MessageResponse(BaseModel):
    id: UUID
    conversation_id: UUID
    sender: UserBasic
    content: str
    timestamp: datetime
