from pydantic import BaseModel
from uuid import UUID
from typing import List, Optional
from datetime import datetime

class ConversationCreate(BaseModel):
    name: str
    details: Optional[str] = None
    user_ids: List[UUID]  # List of user IDs to be added to the conversation

class ConversationResponse(BaseModel):
    id: UUID
    name: str
    details: Optional[str]
    created_by: UUID
    created_at: datetime
    user_ids: List[UUID] 

    class Config:
        from_attributes = True
