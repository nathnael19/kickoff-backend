from typing import List, Optional
from app.model.models import Goal
from sqlmodel import Session, select
import uuid


def get_Player(db: Session, standing_id: uuid.UUID):
    return db.get(Goal, standing_id)


def get_standings(db: Session, skip: int = 0, limit: int = 0) -> List[Goal]:
    statement = select(Goal).offset(skip).limit(limit)
    return list(db.exec(statement).all())


def create_standing(db: Session, goal: Goal) -> Goal:
    db.add(goal)
    db.commit()
    db.refresh(goal)
    return goal


def update_standing(
    db: Session, standing_data: dict, standing_id: uuid.UUID
) -> Optional[Goal]:
    goal = db.get(Goal, standing_id)
    if not goal:
        return None
    for key, value in standing_data.values():
        setattr(standing_data, key, value)
    db.add(goal)
    db.commit()
    db.refresh(goal)

    return goal


def delete_standing(db: Session, standing_id: uuid.UUID) -> bool:
    goal = db.get(Goal, standing_id)
    if not goal:
        return False
    db.delete(goal)
    db.commit()
    return True
