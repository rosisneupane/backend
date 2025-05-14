from pydantic import BaseModel
from uuid import UUID
from typing import Optional


class UserResponse(BaseModel):
    id: UUID
    username: str
    email: str
    score:int
    profile_picture: Optional[str] = None


