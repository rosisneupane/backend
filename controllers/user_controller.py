from fastapi import APIRouter, Depends, HTTPException,Request,Query
from sqlalchemy.orm import Session
from schemas.user_schema import UserResponse
from models.user_model import User
from database.database import get_db
from typing import List
from middleware.auth_middleware import get_current_user

router = APIRouter(prefix="/user", tags=["User"])
 


@router.get("/", response_model=List[UserResponse])
def get_users(current_user: str = Depends(get_current_user),db: Session = Depends(get_db)):
    return db.query(User).filter(User.id != current_user).all()

@router.get("/all", response_model=List[UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@router.get("/me", response_model=UserResponse)
def get_user_details(current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == current_user).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/score", response_model=UserResponse)
def update_user_score(
    new_score: int = Query(..., description="The new score to set for the user"),
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    user = db.query(User).filter(User.id == current_user).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.score = new_score
    db.commit()
    db.refresh(user)

    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        score=user.score
    )