from typing import List, Optional
from sqlmodel import Session, select
from app.model.models import Tournament
import uuid

from app.utils.helpers import add_to_db, delete_from_db


def get_tournament(db: Session, tournament_id: uuid.UUID) -> Optional[Tournament]:
    return db.get(Tournament, tournament_id)


def get_tournaments(db: Session, skip: int = 0, limit: int = 0) -> List[Tournament]:
    statement = select(Tournament).offset(skip).limit(limit)
    return list(db.exec(statement).all())


def create_tournament(db: Session, tournament: Tournament) -> Tournament:
    return add_to_db(db, tournament)


def update_tournament(
    db: Session, tournament_id: uuid.UUID, tournament_data: dict
) -> Optional[Tournament]:
    tournament = db.get(Tournament, tournament_id)
    if not tournament:
        return None
    for key, value in tournament_data.items():
        setattr(tournament, key, value)
    return add_to_db(db, tournament)


def delete_tournament(db: Session, tournament_id: uuid.UUID):
    return delete_from_db(db=db, id=tournament_id, model=Tournament)
