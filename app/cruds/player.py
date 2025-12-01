from typing import List, Optional
from app.model.models import Player
from sqlmodel import Session, select
import uuid


def get_Player(db: Session, player_id: uuid.UUID):
    return db.get(Player, player_id)


def get_players(db: Session, skip: int = 0, limit: int = 0) -> List[Player]:
    statement = select(Player).offset(skip).limit(limit)
    return list(db.exec(statement).all())


def create_player(db: Session, player: Player) -> Player:
    db.add(player)
    db.commit()
    db.refresh(player)
    return player


def update_player(
    db: Session, player_data: dict, player_id: uuid.UUID
) -> Optional[Player]:
    player = db.get(Player, player_id)
    if not player:
        return None
    for key, value in player_data.items():
        setattr(player_data, key, value)
    db.add(player)
    db.commit()
    db.refresh(player)

    return player


def delete_player(db: Session, player_id: uuid.UUID) -> bool:
    player = db.get(Player, player_id)
    if not player:
        return False
    db.delete(player)
    db.commit()
    return True
