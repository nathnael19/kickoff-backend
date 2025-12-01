from typing import List, Optional
from sqlmodel import Session, select
from app.model.models import Tournament
import uuid


def get_tournament(db: Session, tournament_id: uuid.UUID) -> Optional[Tournament]:
    return db.get(Tournament, tournament_id)


def get_tournaments(db: Session, skip: int = 0, limit: int = 0) -> List[Tournament]:
    statement = select(Tournament).offset(skip).limit(limit)
    return list(db.exec(statement).all())


def create_tournament(db: Session, tournament: Tournament) -> Tournament:
    db.add(tournament)
    db.commit()
    db.refresh(tournament)
    return tournament


def update_tournament(
    db: Session, tournament_id: uuid.UUID, tournament_data: dict
) -> Optional[Tournament]:
    tournament = db.get(Tournament, tournament_id)
    if not tournament:
        return None
    for key, value in tournament_data.items():
        setattr(tournament, key, value)
    db.add(tournament)
    db.commit()
    db.refresh(tournament)
    return tournament


def delete_tournament(db: Session, tournament_id: uuid.UUID) -> bool:
    tournament = db.get(Tournament, tournament_id)
    if not tournament:
        return False
    db.delete(tournament)
    db.commit()
    return True
