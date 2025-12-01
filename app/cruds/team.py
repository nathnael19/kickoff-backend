from typing import List, Optional
from sqlmodel import Session, select
from app.model.models import Team
import uuid

from app.utils.helpers import add_to_db, delete_from_db, update_to_db


def get_team(db: Session, team_id: uuid.UUID) -> Optional[Team]:
    return db.get(Team, team_id)


def get_teams(db: Session, skip: int = 0, limit: int = 0) -> List[Team]:
    statement = select(Team).offset(skip).limit(limit)
    return list(db.exec(statement).all())


def create_team(db: Session, team: Team) -> Team:
    return add_to_db(db, team)


def update_team(db: Session, team_id: uuid.UUID, team_data: dict) -> Optional[Team]:
    return update_to_db(db, team_id, team_data, Team)


def delete_team(db: Session, team_id: uuid.UUID) -> bool:
    return delete_from_db(db, team_id, Team)
