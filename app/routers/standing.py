from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List, Optional
from app.database.db import get_session
from app.model.models import Standing
import uuid
from app.cruds.standing import (
    create_standing,
    get_standing,
    get_standings,
    update_standing,
    delete_standing,
)

router = APIRouter(prefix="/standings", tags=["Standings"])


@router.get("/", response_model=List[Standing])
def read_standings(db: Session = Depends(get_session), skip: int = 0, limit: int = 100):
    return get_standings(db=db, skip=skip, limit=limit)


@router.get("/{standing_id}", response_model=Standing)
def read_standing(standing_id: uuid.UUID, db: Session = Depends(get_session)):
    standing = get_standing(db=db, standing_id=standing_id)
    if not standing:
        raise HTTPException(detail="Not found!", status_code=status.HTTP_404_NOT_FOUND)
    return standing


@router.post("/", response_model=Standing)
def add_standing(standing: Standing, db: Session = Depends(get_session)):
    return create_standing(db=db, standing=standing)


@router.put("/", response_model=Standing)
def put_standing(
    standing_id: uuid.UUID, standing_data: dict, db: Session = Depends(get_session)
):
    update = update_standing(
        db=db, standing_id=standing_id, standing_data=standing_data
    )
    if not update:
        raise HTTPException(detail="Not Found!!", status_code=status.HTTP_404_NOT_FOUND)
    return update


@router.delete("/", response_model=dict)
def remove_standing(standing_id: uuid.UUID, db: Session = Depends(get_session)):
    delete = delete_standing(db=db, standing_id=standing_id)
    if not delete:
        raise HTTPException(detail="Not Found!!", status_code=status.HTTP_404_NOT_FOUND)
    return {"ok": True}
