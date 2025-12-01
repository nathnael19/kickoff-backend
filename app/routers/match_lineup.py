from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.model.models import MatchLineup, MatchLineupCreate
import uuid
from app.utils.helpers import database_dependency
from app.cruds.match_lineup import (
    create_match_lineup,
    get_match_lineup,
    get_match_lineups,
    update_match_lineup,
    delete_match_lineup,
)

router = APIRouter(prefix="/match_lineups", tags=["Match Lineups"])


@router.get("/", response_model=List[MatchLineup])
def read_match_lineups(db: database_dependency, skip: int = 0, limit: int = 100):
    return get_match_lineups(db=db, skip=skip, limit=limit)


@router.get("/{match_lineup_id}", response_model=MatchLineup)
def read_match_lineup(match_lineup_id: uuid.UUID, db: database_dependency):
    match_lineup = get_match_lineup(db=db, match_lineup_id=match_lineup_id)
    if not match_lineup:
        raise HTTPException(detail="Not found!", status_code=status.HTTP_404_NOT_FOUND)
    return match_lineup


@router.post("/", response_model=MatchLineup)
def add_match_lineup(match_lineup: MatchLineupCreate, db: database_dependency):
    return create_match_lineup(db=db, match_lineup=match_lineup)


@router.put("/", response_model=MatchLineup)
def put_match_lineup(
    match_lineup_id: uuid.UUID,
    match_lineup_data: dict,
    db: database_dependency,
):
    update = update_match_lineup(
        db=db, match_lineup_id=match_lineup_id, match_lineup_data=match_lineup_data
    )
    if not update:
        raise HTTPException(detail="Not Found!!", status_code=status.HTTP_404_NOT_FOUND)
    return update


@router.delete("/", response_model=dict)
def remove_match_lineup(match_lineup_id: uuid.UUID, db: database_dependency):
    delete = delete_match_lineup(db=db, match_lineup_id=match_lineup_id)
    if not delete:
        raise HTTPException(detail="Not Found!!", status_code=status.HTTP_404_NOT_FOUND)
    return {"ok": True}
