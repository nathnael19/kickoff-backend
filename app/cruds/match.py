from typing import List, Optional
from app.model.models import Match
from sqlmodel import Session, select
import uuid


def get_Player(db: Session, standing_id: uuid.UUID):
    return db.get(Match, standing_id)


def get_standings(db: Session, skip: int = 0, limit: int = 0) -> List[Match]:
    statement = select(Match).offset(skip).limit(limit)
    return list(db.exec(statement).all())


def create_standing(db: Session, match: Match) -> Match:
    db.add(match)
    db.commit()
    db.refresh(match)
    return match


def update_standing(
    db: Session, standing_data: dict, standing_id: uuid.UUID
) -> Optional[Match]:
    match = db.get(Match, standing_id)
    if not match:
        return None
    for key, value in standing_data.values():
        setattr(standing_data, key, value)
    db.add(match)
    db.commit()
    db.refresh(match)

    return match


def delete_standing(db: Session, standing_id: uuid.UUID) -> bool:
    match = db.get(Match, standing_id)
    if not match:
        return False
    db.delete(match)
    db.commit()
    return True
