from sqlmodel import select
from sqlalchemy.orm import selectinload
from sqlmodel import Session
import uuid
from datetime import datetime
from typing import List, Optional
from sqlmodel import Session, select
from app.model.models import Tournament, TournamentCreate
import uuid

from app.utils.helpers import add_to_db, delete_from_db, update_to_db


def get_tournament(db: Session, tournament_id: uuid.UUID) -> Optional[Tournament]:
    return db.get(Tournament, tournament_id)


def get_tournaments(db: Session, skip: int = 0, limit: int = 0) -> List[Tournament]:
    statement = select(Tournament).offset(skip).limit(limit)
    return list(db.exec(statement).all())


def create_tournament(db: Session, tournament: TournamentCreate) -> Tournament:
    db_tournament = Tournament.model_validate(tournament)
    return add_to_db(db, db_tournament)


def update_tournament(
    db: Session, tournament_id: uuid.UUID, tournament_data: dict
) -> Optional[Tournament]:
    tournament_data["updated_at"] = datetime.now()
    return update_to_db(db, tournament_id, tournament_data, Tournament)


def delete_tournament(db: Session, tournament_id: uuid.UUID):
    return delete_from_db(db=db, id=tournament_id, model=Tournament)


def get_tournament_full(db: Session, tournament_id: uuid.UUID):
    statement = (
        select(Tournament)
        .where(Tournament.id == tournament_id)
        .options(selectinload(Tournament.teams))  # type: ignore
    )
    result = db.exec(statement).first()
    return result
