from fastapi import APIRouter, Depends, HTTPException,Request,Form
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from schemas.video_schema import CollectionMain,CollectionCreate,CollectionUpdate
from models.video_model import Collection
from database.database import get_db
from middleware.auth_middleware import get_current_user
from fastapi.responses import RedirectResponse
from starlette import status

router = APIRouter(prefix="/collections", tags=["Collections"])

@router.post("/")
def create_collection(request: Request,name: str = Form(...),description: str = Form(None),db: Session = Depends(get_db),current_user: str = Depends(get_current_user)):
    new_collection = Collection(name=name, description=description)
    db.add(new_collection)
    db.commit()
    db.refresh(new_collection)
    return RedirectResponse(url="/admin/videos", status_code=status.HTTP_302_FOUND)

@router.get("/", response_model=List[CollectionMain])
def get_collections(db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    return db.query(Collection).all()

@router.get("/{collection_id}", response_model=CollectionMain)
def get_collection(collection_id: UUID, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    collection = db.query(Collection).filter(Collection.id == collection_id).first()
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    return collection

@router.put("/{collection_id}", response_model=CollectionMain)
def update_collection(collection_id: UUID, collection_data: CollectionUpdate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    collection = db.query(Collection).filter(Collection.id == collection_id).first()
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    for key, value in collection_data.dict().items():
        setattr(collection, key, value)
    db.commit()
    db.refresh(collection)
    return collection

@router.delete("/{collection_id}")
def delete_collection(collection_id: UUID, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    collection = db.query(Collection).filter(Collection.id == collection_id).first()
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    db.delete(collection)
    db.commit()
    return {"detail": "Collection deleted"}


@router.post("/delete/{collection_id}")
async def delete_collection(
    collection_id: UUID,
    db: Session = Depends(get_db),
):
    collection = db.query(Collection).filter(Collection.id == collection_id).first()
    if collection:
        db.delete(collection)
        db.commit()
    return RedirectResponse(url="/admin/videos", status_code=302)

