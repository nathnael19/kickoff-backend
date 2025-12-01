from typing import List, Optional
from app.model.models import Goal
from sqlmodel import Session, select
import uuid

from app.utils.helpers import add_to_db


def get_goal(db: Session, goal_id: uuid.UUID):
    return db.get(Goal, goal_id)


def get_goals(db: Session, skip: int = 0, limit: int = 0) -> List[Goal]:
    statement = select(Goal).offset(skip).limit(limit)
    return list(db.exec(statement).all())


def create_goal(db: Session, goal: Goal) -> Goal:
    return add_to_db(db, goal)


def update_goal(db: Session, goal_data: dict, goal_id: uuid.UUID) -> Optional[Goal]:
    goal = db.get(Goal, goal_id)
    if not goal:
        return None
    for key, value in goal_data.items():
        setattr(goal, key, value)
    return add_to_db(db, goal)


def delete_goal(db: Session, goal_id: uuid.UUID) -> bool:
    goal = db.get(Goal, goal_id)
    if not goal:
        return False
    db.delete(goal)
    db.commit()
    return True
