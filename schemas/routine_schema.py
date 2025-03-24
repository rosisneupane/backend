from pydantic import BaseModel
from datetime import date, time
import uuid

class RoutineCreate(BaseModel):
    date: date
    time: time
    text: str
    status: bool = False  # Default to False (incomplete)

class RoutineResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    date: date
    time: time
    text: str
    status: bool

    class Config:
        from_attributes = True
