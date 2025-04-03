from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import get_db
from models.mood_model import Mood
from models.user_model import User
from schemas.mood_schema import MoodCreate, MoodResponse
from middleware.auth_middleware import get_current_user
from typing import List
from datetime import date
from uuid import UUID


router = APIRouter(prefix="/mood", tags=["Mood"])
# Create a new mood
@router.post("/mood", response_model=MoodResponse)
def create_mood(mood: MoodCreate, current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    # Check if mood already exists for the day
    existing_mood = db.query(Mood).filter(
        Mood.user_id == current_user,
        Mood.date == date.today()
    ).first()

    if existing_mood:
        raise HTTPException(status_code=400, detail="Mood for today already exists")

    new_mood = Mood(
        user_id=current_user,
        date=date.today(),
        mood_rating=mood.mood_rating
    )
    db.add(new_mood)
    db.commit()
    db.refresh(new_mood)
    return new_mood

# Get all moods for the current user
@router.get("/mood", response_model=List[MoodResponse])
def get_all_moods(current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    moods = db.query(Mood).filter(Mood.user_id == current_user).order_by(Mood.date.desc()).all()
    return moods

@router.delete("/mood/{mood_id}", status_code=200)
def delete_mood(mood_id: str, current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        # Convert mood_id to UUID
        mood_uuid = UUID(mood_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")

    # Query with the correct UUID type
    mood = db.query(Mood).filter(Mood.id == mood_uuid, Mood.user_id == current_user).first()
    
    if not mood:
        raise HTTPException(status_code=404, detail="Mood not found")
    
    db.delete(mood)
    db.commit()
    return {"detail": "Mood deleted successfully"}


@router.get("/mood/today/exist", response_model=bool)
def check_today_mood(current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    # Query for today's mood
    exists = db.query(Mood).filter(
        Mood.user_id == current_user,
        Mood.date == date.today()
    ).first()
    return bool(exists)
