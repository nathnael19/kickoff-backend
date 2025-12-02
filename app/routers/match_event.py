from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.model.models import MatchEvent, MatchEventCreate
import uuid
from app.core.dep import get_current_user
from app.utils.helpers import database_dependency
from app.cruds.match_event import (
    create_match_event,
    get_match_event,
    get_match_events,
    update_match_event,
    delete_match_event,
)

router = APIRouter(prefix="/match_events", tags=["MatchEvents"])


@router.get("/", response_model=List[MatchEvent])
def read_match_events(db: database_dependency, skip: int = 0, limit: int = 100):
    return get_match_events(db=db, skip=skip, limit=limit)


@router.get("/{match_event_id}", response_model=MatchEvent)
def read_match_event(
    match_event_id: uuid.UUID, db: database_dependency, user=Depends(get_current_user)
):
    match_event = get_match_event(db=db, match_event_id=match_event_id)
    if not match_event:
        raise HTTPException(detail="Not found!", status_code=status.HTTP_404_NOT_FOUND)
    return match_event


@router.post("/", response_model=MatchEvent)
def add_match_event(
    match_event: MatchEventCreate,
    db: database_dependency,
    user=Depends(get_current_user),
):
    return create_match_event(db=db, match_event=match_event)


@router.put("/", response_model=MatchEvent)
def put_match_event(
    match_event_id: uuid.UUID,
    match_event_data: dict,
    db: database_dependency,
    user=Depends(get_current_user),
):
    update = update_match_event(
        db=db, match_event_id=match_event_id, match_event_data=match_event_data
    )
    if not update:
        raise HTTPException(detail="Not Found!!", status_code=status.HTTP_404_NOT_FOUND)
    return update


@router.delete("/", response_model=dict)
def remove_match_event(
    match_event_id: uuid.UUID, db: database_dependency, user=Depends(get_current_user)
):
    delete = delete_match_event(db=db, match_event_id=match_event_id)
    if not delete:
        raise HTTPException(detail="Not Found!!", status_code=status.HTTP_404_NOT_FOUND)
    return {"ok": True}
