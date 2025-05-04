from pydantic import BaseModel
from uuid import UUID

class PdfMain(BaseModel):
    id: UUID
    type: str
    title: str
    url: str

    class Config:
        orm_mode = True
