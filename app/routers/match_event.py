from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List, Optional
from app.database.db import get_session
from app.model.models import MatchEvent
import uuid
from app.cruds.match_event import (
    create_match_event,
    get_match_event,
    get_match_events,
    update_match_event,
    delete_match_event,
)

router = APIRouter(prefix="/match_events", tags=["MatchEvents"])


@router.get("/", response_model=List[MatchEvent])
def read_match_events(
    db: Session = Depends(get_session), skip: int = 0, limit: int = 100
):
    return get_match_events(db=db, skip=skip, limit=limit)


@router.get("/{match_event_id}", response_model=MatchEvent)
def read_match_event(match_event_id: uuid.UUID, db: Session = Depends(get_session)):
    match_event = get_match_event(db=db, match_event_id=match_event_id)
    if not match_event:
        raise HTTPException(detail="Not found!", status_code=status.HTTP_404_NOT_FOUND)
    return match_event


@router.post("/", response_model=MatchEvent)
def add_match_event(match_event: MatchEvent, db: Session = Depends(get_session)):
    return create_match_event(db=db, match_event=match_event)


@router.put("/", response_model=MatchEvent)
def put_match_event(
    match_event_id: uuid.UUID,
    match_event_data: dict,
    db: Session = Depends(get_session),
):
    update = update_match_event(
        db=db, match_event_id=match_event_id, match_event_data=match_event_data
    )
    if not update:
        raise HTTPException(detail="Not Found!!", status_code=status.HTTP_404_NOT_FOUND)
    return update


@router.delete("/", response_model=dict)
def remove_match_event(match_event_id: uuid.UUID, db: Session = Depends(get_session)):
    delete = delete_match_event(db=db, match_event_id=match_event_id)
    if not delete:
        raise HTTPException(detail="Not Found!!", status_code=status.HTTP_404_NOT_FOUND)
    return {"ok": True}
