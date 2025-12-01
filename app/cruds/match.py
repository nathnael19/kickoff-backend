from datetime import datetime
from typing import List, Optional
from app.model.models import Match, MatchCreate
from sqlmodel import Session, select
import uuid

from app.utils.helpers import add_to_db, delete_from_db, update_to_db


def get_match(db: Session, match_id: uuid.UUID):
    return db.get(Match, match_id)


def get_matchs(db: Session, skip: int = 0, limit: int = 0) -> List[Match]:
    statement = select(Match).offset(skip).limit(limit)
    return list(db.exec(statement).all())


def create_match(db: Session, match: MatchCreate) -> Match:
    db_match = Match.model_validate(match)
    return add_to_db(db, db_match)


def update_match(db: Session, match_data: dict, match_id: uuid.UUID) -> Optional[Match]:
    match_data["updated_at"] = datetime.now()
    return update_to_db(db, match_id, match_data, Match)


def delete_match(db: Session, match_id: uuid.UUID) -> bool:
    return delete_from_db(db, match_id, Match)
