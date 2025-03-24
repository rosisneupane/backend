from pydantic import BaseModel
from datetime import date
from uuid import UUID

# Schema for creating a mood
class MoodCreate(BaseModel):
    mood_rating: int  # 1 to 5

    class Config:
        orm_mode = True

# Schema for response
class MoodResponse(BaseModel):
    id: UUID
    user_id: UUID
    date: date
    mood_rating: int

    class Config:
        orm_mode = True
