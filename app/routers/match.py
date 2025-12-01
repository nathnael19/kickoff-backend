from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.model.models import Match, MatchCreate
import uuid
from app.utils.helpers import database_dependency
from app.cruds.match import (
    create_match,
    get_match,
    get_matchs,
    update_match,
    delete_match,
)

router = APIRouter(prefix="/matches", tags=["Matches"])


@router.get("/", response_model=List[Match])
def read_matchs(db: database_dependency, skip: int = 0, limit: int = 100):
    return get_matchs(db=db, skip=skip, limit=limit)


@router.get("/{match_id}", response_model=Match)
def read_match(match_id: uuid.UUID, db: database_dependency):
    match = get_match(db=db, match_id=match_id)
    if not match:
        raise HTTPException(detail="Not found!", status_code=status.HTTP_404_NOT_FOUND)
    return match


@router.post("/", response_model=Match)
def add_match(match: MatchCreate, db: database_dependency):
    return create_match(db=db, match=match)


@router.put("/", response_model=Match)
def put_match(match_id: uuid.UUID, match_data: dict, db: database_dependency):
    update = update_match(db=db, match_id=match_id, match_data=match_data)
    if not update:
        raise HTTPException(detail="Not Found!!", status_code=status.HTTP_404_NOT_FOUND)
    return update


@router.delete("/", response_model=dict)
def remove_match(match_id: uuid.UUID, db: database_dependency):
    delete = delete_match(db=db, match_id=match_id)
    if not delete:
        raise HTTPException(detail="Not Found!!", status_code=status.HTTP_404_NOT_FOUND)
    return {"ok": True}
