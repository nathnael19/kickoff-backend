from typing import List, Optional
from app.model.models import MatchEvent
from sqlmodel import Session, select
import uuid


def get_Player(db: Session, match_event_id: uuid.UUID):
    return db.get(MatchEvent, match_event_id)


def get_match_events(db: Session, skip: int = 0, limit: int = 0) -> List[MatchEvent]:
    statement = select(MatchEvent).offset(skip).limit(limit)
    return list(db.exec(statement).all())


def create_match_event(db: Session, match_event: MatchEvent) -> MatchEvent:
    db.add(match_event)
    db.commit()
    db.refresh(match_event)
    return match_event


def update_match_event(
    db: Session, match_event_data: dict, match_event_id: uuid.UUID
) -> Optional[MatchEvent]:
    match_event = db.get(MatchEvent, match_event_id)
    if not match_event:
        return None
    for key, value in match_event_data.values():
        setattr(match_event_data, key, value)
    db.add(match_event)
    db.commit()
    db.refresh(match_event)

    return match_event


def delete_match_event(db: Session, match_event_id: uuid.UUID) -> bool:
    match_event = db.get(MatchEvent, match_event_id)
    if not match_event:
        return False
    db.delete(match_event)
    db.commit()
    return True
