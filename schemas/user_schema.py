from pydantic import BaseModel
from uuid import UUID


class UserResponse(BaseModel):
    id: UUID
    username: str
    email: str
    score:int


