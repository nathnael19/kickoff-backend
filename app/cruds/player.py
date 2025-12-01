from typing import List, Optional
from app.model.models import Player
from sqlmodel import Session, select
import uuid


def get_Player(db: Session, standing_id: uuid.UUID):
    return db.get(Player, standing_id)


def get_standings(db: Session, skip: int = 0, limit: int = 0) -> List[Player]:
    statement = select(Player).offset(skip).limit(limit)
    return list(db.exec(statement).all())


def create_standing(db: Session, player: Player) -> Player:
    db.add(player)
    db.commit()
    db.refresh(player)
    return player


def update_standing(
    db: Session, standing_data: dict, standing_id: uuid.UUID
) -> Optional[Player]:
    player = db.get(Player, standing_id)
    if not player:
        return None
    for key, value in standing_data.values():
        setattr(standing_data, key, value)
    db.add(player)
    db.commit()
    db.refresh(player)

    return player


def delete_standing(db: Session, standing_id: uuid.UUID) -> bool:
    player = db.get(Player, standing_id)
    if not player:
        return False
    db.delete(player)
    db.commit()
    return True
