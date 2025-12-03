from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from typing import List
from app.model.models import Team, TeamCreate
import uuid
from app.core.dep import get_current_user
from app.utils.helpers import database_dependency, upload_to_supabase
from app.cruds.team import create_team, get_team, get_teams, update_team, delete_team

router = APIRouter(prefix="/teams", tags=["Teams"])


@router.get("/", response_model=List[Team])
def read_teams(db: database_dependency, skip: int = 0, limit: int = 100):
    return get_teams(db=db, skip=skip, limit=limit)


@router.get("/{team_id}", response_model=Team)
def read_team(team_id: uuid.UUID, db: database_dependency):
    team = get_team(db=db, team_id=team_id)
    if not team:
        raise HTTPException(detail="Not found!", status_code=status.HTTP_404_NOT_FOUND)
    return team


@router.post("/upload")
async def upload_logo(
    db: database_dependency,
    file: UploadFile = File(...),
    team_id: uuid.UUID = Form(...),
):
    url = await upload_to_supabase(file, "teams")
    update_team(db, team_id, {"logo_url": url})
    return {"team_id": team_id, "logo_url": url}


@router.post("/", response_model=Team)
def add_team(team: TeamCreate, db: database_dependency, user=Depends(get_current_user)):
    return create_team(db=db, team=team)


@router.put("/", response_model=Team)
def put_team(
    team_id: uuid.UUID,
    team_data: dict,
    db: database_dependency,
    user=Depends(get_current_user),
):
    update = update_team(db=db, team_id=team_id, team_data=team_data)
    if not update:
        raise HTTPException(detail="Not Found!!", status_code=status.HTTP_404_NOT_FOUND)
    return update


@router.delete("/", response_model=dict)
def remove_team(
    team_id: uuid.UUID, db: database_dependency, user=Depends(get_current_user)
):
    delete = delete_team(db=db, team_id=team_id)
    if not delete:
        raise HTTPException(detail="Not Found!!", status_code=status.HTTP_404_NOT_FOUND)
    return {"ok": True}
