from datetime import date, time
from uuid import UUID as UUIDType
from pydantic import BaseModel


class EventBase(BaseModel):
    title: str
    description: str | None = None
    date: date
    time: time


class EventCreate(EventBase):
    pass


class EventUpdate(EventBase):
    pass


class EventMain(EventBase):
    id: UUIDType

    class Config:
        orm_mode = True
