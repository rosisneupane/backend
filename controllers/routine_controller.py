from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import get_db
from models.user_model import User,Routine
from schemas.routine_schema import RoutineCreate, RoutineResponse
from middleware.auth_middleware import get_current_user
import uuid

router = APIRouter(prefix="/routines", tags=["Routines"])

@router.post("/", response_model=RoutineResponse)
def create_routine(
    routine_data: RoutineCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    routine = Routine(
        id=uuid.uuid4(),
        user_id=current_user,
        date=routine_data.date,
        time=routine_data.time,
        text=routine_data.text,
        status=False
    )
    db.add(routine)
    db.commit()
    db.refresh(routine)
    return routine

@router.get("/", response_model=list[RoutineResponse])
def get_routines(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    routines = db.query(Routine).filter(Routine.user_id == current_user).all()
    return routines

@router.get("/{routine_id}", response_model=RoutineResponse)
def get_routine(
    routine_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    routine = db.query(Routine).filter(Routine.id == routine_id, Routine.user_id == current_user).first()
    if not routine:
        raise HTTPException(status_code=404, detail="Routine not found")
    return routine

@router.put("/{routine_id}", response_model=RoutineResponse)
def update_routine(
    routine_id: uuid.UUID,
    routine_data: RoutineCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    routine = db.query(Routine).filter(Routine.id == routine_id, Routine.user_id == current_user).first()
    if not routine:
        raise HTTPException(status_code=404, detail="Routine not found")
    
    routine.date = routine_data.date
    routine.time = routine_data.time
    routine.text = routine_data.text
    routine.status = routine_data.status
    
    db.commit()
    db.refresh(routine)
    return routine

@router.delete("/{routine_id}")
def delete_routine(
    routine_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    routine = db.query(Routine).filter(Routine.id == routine_id, Routine.user_id == current_user).first()
    if not routine:
        raise HTTPException(status_code=404, detail="Routine not found")
    
    db.delete(routine)
    db.commit()
    return {"detail": "Routine deleted successfully"}
