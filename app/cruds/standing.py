from datetime import datetime
from typing import List, Optional
from app.model.models import Standing, StandingCreate
from sqlmodel import Session, select
import uuid

from app.utils.helpers import add_to_db, delete_from_db, update_to_db


def get_standing(db: Session, standing_id: uuid.UUID):
    return db.get(Standing, standing_id)


def get_standings(db: Session, skip: int = 0, limit: int = 0) -> List[Standing]:
    statement = select(Standing).offset(skip).limit(limit)
    return list(db.exec(statement).all())


def create_standing(db: Session, standing: StandingCreate) -> Standing:
    db_standing = Standing.model_validate(standing)
    return add_to_db(db, db_standing)


def update_standing(
    db: Session, standing_data: dict, standing_id: uuid.UUID
) -> Optional[Standing]:
    standing_data["updated_at"] = datetime.now()
    return update_to_db(db, standing_id, standing_data, Standing)


def delete_standing(db: Session, standing_id: uuid.UUID) -> bool:
    return delete_from_db(db, standing_id, Standing)
