from typing import List, Optional
from app.model.models import MatchLineup
from sqlmodel import Session, select
import uuid


def get_Player(db: Session, match_lineup_id: uuid.UUID):
    return db.get(MatchLineup, match_lineup_id)


def get_match_lineups(db: Session, skip: int = 0, limit: int = 0) -> List[MatchLineup]:
    statement = select(MatchLineup).offset(skip).limit(limit)
    return list(db.exec(statement).all())


def create_match_lineup(db: Session, match_lineup: MatchLineup) -> MatchLineup:
    db.add(match_lineup)
    db.commit()
    db.refresh(match_lineup)
    return match_lineup


def update_match_lineup(
    db: Session, match_lineup_data: dict, match_lineup_id: uuid.UUID
) -> Optional[MatchLineup]:
    match_lineup = db.get(MatchLineup, match_lineup_id)
    if not match_lineup:
        return None
    for key, value in match_lineup_data.values():
        setattr(match_lineup_data, key, value)
    db.add(match_lineup)
    db.commit()
    db.refresh(match_lineup)

    return match_lineup


def delete_match_lineup(db: Session, match_lineup_id: uuid.UUID) -> bool:
    match_lineup = db.get(MatchLineup, match_lineup_id)
    if not match_lineup:
        return False
    db.delete(match_lineup)
    db.commit()
    return True
