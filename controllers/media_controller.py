from fastapi import APIRouter, Depends, HTTPException,Request,Form,UploadFile, File,Query
from sqlalchemy.orm import Session
from uuid import UUID
import uuid
from schemas.media_schema import MediaOut
from models.media_model import Media
from database.database import get_db
from middleware.auth_middleware import get_current_user
from typing import List
from fastapi.responses import RedirectResponse
import shutil
import cloudinary.uploader

router = APIRouter(prefix="/media", tags=["Media"])

@router.post("/upload")
def upload_media(
    category: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    # Extract and clean title
    original_filename = file.filename
    title = original_filename.rsplit(".", 1)[0].replace("_", " ").replace("-", " ").strip()

    # Determine media type
    extension = original_filename.rsplit(".", 1)[-1].lower()
    if extension in ["pdf"]:
        media_type = "pdf"
        resource_type = "raw"
    elif extension in ["mp4", "mov", "avi", "mkv"]:
        media_type = "video"
        resource_type = "video"
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    # Upload to Cloudinary
    try:
        result = cloudinary.uploader.upload(
            file.file,
            resource_type=resource_type,
            folder=f"{category}/",
            public_id=title,
            use_filename=True,
            unique_filename=False,
            overwrite=True
        )
        file_url = result["secure_url"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload to Cloudinary failed: {str(e)}")

    # Save media info to DB
    new_media = Media(
        media_type=media_type,
        category=category,
        title=title,
        url=file_url,
    )
    db.add(new_media)
    db.commit()
    db.refresh(new_media)

    return RedirectResponse(url="/admin/media", status_code=303)


# @router.post("/upload") 
# def upload_media(
#     category: str = Form(...),    # e.g., 'self-help', 'meditation'
#     file: UploadFile = File(...),
#     db: Session = Depends(get_db),
# ):
#     # Extract and clean title from filename
#     original_filename = file.filename
#     title = original_filename.rsplit(".", 1)[0].replace("_", " ").replace("-", " ").strip()

#     # Infer media_type from file extension
#     extension = original_filename.rsplit(".", 1)[-1].lower()
#     if extension in ["pdf"]:
#         media_type = "pdf"
#     elif extension in ["mp4", "mov", "avi", "mkv"]:
#         media_type = "video"
#     else:
#         raise HTTPException(status_code=400, detail="Unsupported file type")

#     # Save file to local storage
#     file_location = f"uploads/{original_filename}"
#     with open(file_location, "wb") as f:
#         shutil.copyfileobj(file.file, f)

#     # Create URL path for stored file
#     file_url = f"/uploads/{original_filename}"

#     # Create and save Media entry
#     new_media = Media(
#         media_type=media_type,
#         category=category,
#         title=title,
#         url=file_url,
#     )
#     db.add(new_media)
#     db.commit()
#     db.refresh(new_media)

#     return RedirectResponse(url="/admin/media", status_code=303)



@router.get("/", response_model=List[MediaOut])
def get_media_by_type_and_category(
    media_type: str = Query(..., regex="^(pdf|video)$"),
    category: str = Query(...),
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    return (
        db.query(Media)
        .filter(Media.media_type == media_type, Media.category == category)
        .all()
    )

@router.post("/delete/{media_id}")
def delete_media(
    media_id: UUID,
    db: Session = Depends(get_db),
):
    media = db.query(Media).filter(Media.id == media_id).first()
    if not media:
        raise HTTPException(status_code=404, detail="Media not found")

    db.delete(media)
    db.commit()
    return {"message": f"{media.media_type.capitalize()} deleted successfully"}
