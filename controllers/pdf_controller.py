from fastapi import APIRouter, Depends, HTTPException,Request,Form,UploadFile, File
from sqlalchemy.orm import Session
from uuid import UUID
import uuid
from schemas.pdf_schema import PdfMain
from models.pdf_model import Pdf
from database.database import get_db
from middleware.auth_middleware import get_current_user
from typing import List

import shutil

router = APIRouter(prefix="/pdfs", tags=["Pdfs"])


@router.post("/upload")
def upload_pdf(
    type: str = Form(...),  # Form field!
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    # Extract title from filename (remove extension and clean)
    original_filename = file.filename
    title = original_filename.rsplit(".", 1)[0].replace("_", " ").replace("-", " ").strip()

    # Save file to local storage
    file_location = f"uploads/{original_filename}"
    with open(file_location, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # Store local URL path
    file_url = f"/uploads/{original_filename}" 
    # Create DB entry
    new_pdf = Pdf(
        type=type,
        title=title,
        url=file_url,
        user_id=current_user
    )
    db.add(new_pdf)
    db.commit()
    db.refresh(new_pdf)
    return {"message": "PDF uploaded successfully", "pdf": new_pdf}


@router.get("/", response_model=List[PdfMain])  # PdfMain is a Pydantic response model
def get_pdfs_by_type(
    type: str,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    return db.query(Pdf).filter(Pdf.user_id == current_user, Pdf.type == type).all()


@router.delete("/{pdf_id}")
def delete_pdf(
    pdf_id: UUID,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    print(pdf_id)
    pdf = db.query(Pdf).filter(Pdf.id == pdf_id, Pdf.user_id == current_user).first()
    if not pdf:
        raise HTTPException(status_code=404, detail="PDF not found")

    db.delete(pdf)
    db.commit()
    return {"message": "PDF deleted successfully"}
