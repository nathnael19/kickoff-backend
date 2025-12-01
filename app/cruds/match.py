from typing import List, Optional
from app.model.models import Match
from sqlmodel import Session, select
import uuid


def get_Player(db: Session, match_id: uuid.UUID):
    return db.get(Match, match_id)


def get_matchs(db: Session, skip: int = 0, limit: int = 0) -> List[Match]:
    statement = select(Match).offset(skip).limit(limit)
    return list(db.exec(statement).all())


def create_match(db: Session, match: Match) -> Match:
    db.add(match)
    db.commit()
    db.refresh(match)
    return match


def update_match(db: Session, match_data: dict, match_id: uuid.UUID) -> Optional[Match]:
    match = db.get(Match, match_id)
    if not match:
        return None
    for key, value in match_data.values():
        setattr(match_data, key, value)
    db.add(match)
    db.commit()
    db.refresh(match)

    return match


def delete_match(db: Session, match_id: uuid.UUID) -> bool:
    match = db.get(Match, match_id)
    if not match:
        return False
    db.delete(match)
    db.commit()
    return True
