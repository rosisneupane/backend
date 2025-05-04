from fastapi import APIRouter, Depends, HTTPException,Request,Form,UploadFile, File
from sqlalchemy.orm import Session
from uuid import UUID
import uuid
from schemas.video_schema import VideoMain,VideoCreate,VideoUpdate
from models.video_model import Collection,Video
from database.database import get_db
from middleware.auth_middleware import get_current_user
from typing import List
from fastapi.responses import RedirectResponse
import shutil

router = APIRouter(prefix="/videos", tags=["Videos"])


@router.get("/", response_model=List[VideoMain])
def get_all_videos(db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    return db.query(Video).all()

@router.get("/collection/{collection_id}", response_model=List[VideoMain])
def get_videos_by_collection(collection_id: UUID, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    return db.query(Video).filter(Video.collection_id == collection_id).all()


@router.post("/collection/{collection_id}", response_model=VideoMain)
def add_video(collection_id: UUID, video: VideoCreate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    collection = db.query(Collection).filter(Collection.id == collection_id).first()
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    db_video = Video(**video.dict(), collection_id=collection_id)
    db.add(db_video)
    db.commit()
    db.refresh(db_video)
    return db_video

@router.put("/{video_id}", response_model=VideoMain)
def update_video(video_id: UUID, video_data: VideoUpdate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    video = db.query(Video).filter(Video.id == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    for key, value in video_data.dict().items():
        setattr(video, key, value)
    db.commit()
    db.refresh(video)
    return video

@router.delete("/{video_id}")
def delete_video(video_id: UUID, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    video = db.query(Video).filter(Video.id == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    db.delete(video)
    db.commit()
    return {"detail": "Video deleted"}


@router.post("/delete/{video_id}")
async def delete_video(
    video_id: UUID,
    db: Session = Depends(get_db),
):
    video = db.query(Video).filter(Video.id == video_id).first()
    if video:
        db.delete(video)
        db.commit()
    return RedirectResponse(url="/admin/videos", status_code=302)



@router.post("/add")
async def handle_add_video_upload(
    request: Request,
    title: str = Form(...),
    collection_id: UUID = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    # Save the uploaded file to the uploads directory
    file_ext = file.filename.split('.')[-1]
    unique_filename = f"{uuid.uuid4()}.{file_ext}"
    file_location = f"uploads/{unique_filename}"

    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Store local URL path
    video_url = f"/uploads/{unique_filename}" 

    new_video = Video(title=title, url=video_url, collection_id=collection_id)
    db.add(new_video)
    db.commit()
    db.refresh(new_video)

    return RedirectResponse(url="/admin/videos", status_code=302)
