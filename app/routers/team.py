from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List, Optional
from app.database.db import get_session
from app.model.models import Team
import uuid
from app.cruds.team import create_team, get_team, get_teams, update_team, delete_team

router = APIRouter(prefix="/teams", tags=["Teams"])


@router.get("/", response_model=List[Team])
def read_teams(db: Session = Depends(get_session), skip: int = 0, limit: int = 100):
    return get_teams(db=db, skip=skip, limit=limit)


@router.get("/{team_id}", response_model=Team)
def read_team(team_id: uuid.UUID, db: Session = Depends(get_session)):
    team = get_team(db=db, team_id=team_id)
    if not team:
        raise HTTPException(detail="Not found!", status_code=status.HTTP_404_NOT_FOUND)
    return team


@router.post("/", response_model=Team)
def add_team(team: Team, db: Session = Depends(get_session)):
    return create_team(db=db, team=team)


@router.put("/", response_model=Team)
def put_team(team_id: uuid.UUID, team_data: dict, db: Session = Depends(get_session)):
    update = update_team(db=db, team_id=team_id, team_data=team_data)
    if not update:
        raise HTTPException(detail="Not Found!!", status_code=status.HTTP_404_NOT_FOUND)
    return update


@router.delete("/", response_model=dict)
def remove_team(team_id: uuid.UUID, db: Session = Depends(get_session)):
    delete = delete_team(db=db, team_id=team_id)
    if not delete:
        raise HTTPException(detail="Not Found!!", status_code=status.HTTP_404_NOT_FOUND)
    return {"ok": True}
