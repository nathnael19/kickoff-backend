from typing import List, Optional
from app.model.models import Player
from sqlmodel import Session, select
import uuid

from app.utils.helpers import add_to_db, delete_from_db, update_to_db


def get_player(db: Session, player_id: uuid.UUID):
    return db.get(Player, player_id)


def get_players(db: Session, skip: int = 0, limit: int = 0) -> List[Player]:
    statement = select(Player).offset(skip).limit(limit)
    return list(db.exec(statement).all())


def create_player(db: Session, player: Player) -> Player:
    return add_to_db(db, player)


def update_player(
    db: Session, player_data: dict, player_id: uuid.UUID
) -> Optional[Player]:
    return update_to_db(db, player_id, player_data, Player)


def delete_player(db: Session, player_id: uuid.UUID) -> bool:
    return delete_from_db(db, player_id, Player)
