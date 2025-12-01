from typing import List, Optional
from app.model.models import Standing
from sqlmodel import Session, select
import uuid

from app.utils.helpers import add_to_db


def get_standing(db: Session, standing_id: uuid.UUID):
    return db.get(Standing, standing_id)


def get_standings(db: Session, skip: int = 0, limit: int = 0) -> List[Standing]:
    statement = select(Standing).offset(skip).limit(limit)
    return list(db.exec(statement).all())


def create_standing(db: Session, standing: Standing) -> Standing:
    return add_to_db(db, standing)


def update_standing(
    db: Session, standing_data: dict, standing_id: uuid.UUID
) -> Optional[Standing]:
    standing = db.get(Standing, standing_id)
    if not standing:
        return None
    for key, value in standing_data.items():
        setattr(standing, key, value)
    return add_to_db(db, standing)


def delete_standing(db: Session, standing_id: uuid.UUID) -> bool:
    standing = db.get(Standing, standing_id)
    if not standing:
        return False
    db.delete(standing)
    db.commit()
    return True
