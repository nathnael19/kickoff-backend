from typing import List, Optional
from app.model.models import MatchLineup
from sqlmodel import Session, select
import uuid


def get_Player(db: Session, standing_id: uuid.UUID):
    return db.get(MatchLineup, standing_id)


def get_standings(db: Session, skip: int = 0, limit: int = 0) -> List[MatchLineup]:
    statement = select(MatchLineup).offset(skip).limit(limit)
    return list(db.exec(statement).all())


def create_standing(db: Session, match_lineup: MatchLineup) -> MatchLineup:
    db.add(match_lineup)
    db.commit()
    db.refresh(match_lineup)
    return match_lineup


def update_standing(
    db: Session, standing_data: dict, standing_id: uuid.UUID
) -> Optional[MatchLineup]:
    match_lineup = db.get(MatchLineup, standing_id)
    if not match_lineup:
        return None
    for key, value in standing_data.values():
        setattr(standing_data, key, value)
    db.add(match_lineup)
    db.commit()
    db.refresh(match_lineup)

    return match_lineup


def delete_standing(db: Session, standing_id: uuid.UUID) -> bool:
    match_lineup = db.get(MatchLineup, standing_id)
    if not match_lineup:
        return False
    db.delete(match_lineup)
    db.commit()
    return True
