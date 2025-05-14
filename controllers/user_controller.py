from fastapi import APIRouter, Depends, HTTPException,Request,Query,UploadFile,File
from sqlalchemy.orm import Session
from schemas.user_schema import UserResponse
from models.user_model import User
from database.database import get_db
from typing import List
from middleware.auth_middleware import get_current_user
import cloudinary.uploader

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


@router.post("/upload_profile_picture", response_model=UserResponse)
def upload_profile_picture(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user),  # <-- just the user ID
):
    # Fetch the user from DB
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Validate file type
    extension = file.filename.rsplit(".", 1)[-1].lower()
    if extension not in ["jpg", "jpeg", "png", "webp"]:
        raise HTTPException(status_code=400, detail="Unsupported image format")

    # Upload to Cloudinary
    try:
        result = cloudinary.uploader.upload(
            file.file,
            folder=f"users/{user.id}/profile/",
            public_id="profile_pic",
            use_filename=True,
            unique_filename=False,
            overwrite=True,
        )
        image_url = result["secure_url"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cloudinary upload failed: {str(e)}")

    # Update DB
    user.profile_picture = image_url
    db.commit()
    db.refresh(user)

    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        score=user.score,
        profile_picture=user.profile_picture
    )