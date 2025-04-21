from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional


class AiConversationCreate(BaseModel):
    name: Optional[str] = None


class AiConversationResponse(BaseModel):
    id: UUID
    name: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True


class AiMessageCreate(BaseModel):
    content: str


class AiMessageResponse(BaseModel):
    id: UUID
    sender: str
    content: str
    timestamp: datetime

    class Config:
        orm_mode = True
