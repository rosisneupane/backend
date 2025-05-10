from fastapi import APIRouter, Depends, HTTPException,Form
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from database.database import get_db
from models.event_model import Event
from schemas.event_schema import EventCreate, EventUpdate, EventMain
from typing import List
from uuid import UUID
from datetime import date, time

router = APIRouter(prefix="/events", tags=["Events"])


@router.get("/", response_model=List[EventMain])
def read_events(db: Session = Depends(get_db)):
    return db.query(Event).all()


@router.get("/{event_id}", response_model=EventMain)
def read_event(event_id: UUID, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event


@router.post("/", response_model=EventMain)
def create_event(
    title: str = Form(...),
    description: str = Form(...),
    date: date = Form(...),
    time: time = Form(...),
    db: Session = Depends(get_db)
):
    try:
        new_event = Event(title=title, description=description, date=date, time=time)
        db.add(new_event)
        db.commit()
        db.refresh(new_event)
        return RedirectResponse(url="/admin/events", status_code=303)
    except SQLAlchemyError as e:
        db.rollback()
        logging.error(f"Failed to create event: {e}")
        raise HTTPException(status_code=500, detail="Failed to create event")




@router.put("/{event_id}", response_model=EventMain)
def update_event(event_id: UUID, event_data: EventUpdate, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    for key, value in event_data.dict().items():
        setattr(event, key, value)

    try:
        db.commit()
        db.refresh(event)
        return event
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to update event")


@router.post("/delete/{event_id}", response_model=EventMain)
def delete_event(event_id: UUID, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    try:
        db.delete(event)
        db.commit()
        return event
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to delete event")
