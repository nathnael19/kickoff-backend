from typing import List, Optional
from sqlmodel import Session, select
from app.model.models import Team
import uuid


def get_team(db: Session, team_id: uuid.UUID) -> Optional[Team]:
    return db.get(Team, team_id)


def get_teams(db: Session, skip: int = 0, limit: int = 0) -> List[Team]:
    statement = select(Team).offset(skip).limit(limit)
    return list(db.exec(statement).all())


def create_team(db: Session, team: Team) -> Team:
    db.add(team)
    db.commit()
    db.refresh(team)
    return team


def update_team(db: Session, team_id: uuid.UUID, team_data: dict) -> Optional[Team]:
    team = db.get(Team, team_id)
    if not team:
        return None
    for key, value in team_data.items():
        setattr(team, key, value)
    db.add(team)
    db.commit()
    db.refresh(team)
    return team


def delete_team(db: Session, team_id: uuid.UUID) -> bool:
    team = db.get(Team, team_id)
    if not team:
        return False
    db.delete(team)
    db.commit()
    return True
