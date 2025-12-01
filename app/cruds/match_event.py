from datetime import datetime
from typing import List, Optional
from app.model.models import MatchEvent, MatchEventCreate
from sqlmodel import Session, select
import uuid

from app.utils.helpers import add_to_db, delete_from_db, update_to_db


def get_match_event(db: Session, match_event_id: uuid.UUID):
    return db.get(MatchEvent, match_event_id)


def get_match_events(db: Session, skip: int = 0, limit: int = 0) -> List[MatchEvent]:
    statement = select(MatchEvent).offset(skip).limit(limit)
    return list(db.exec(statement).all())


def create_match_event(db: Session, match_event: MatchEventCreate) -> MatchEvent:
    db_match_event = MatchEvent.model_validate(match_event)
    return add_to_db(db, db_match_event)


def update_match_event(
    db: Session, match_event_data: dict, match_event_id: uuid.UUID
) -> Optional[MatchEvent]:
    match_event_data["updated_at"] = datetime.now()
    return update_to_db(db, match_event_id, match_event_data, MatchEvent)


def delete_match_event(db: Session, match_event_id: uuid.UUID) -> bool:
    return delete_from_db(db, match_event_id, MatchEvent)
