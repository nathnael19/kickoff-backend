from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    File,
    UploadFile,
)
from typing import List
import uuid
from app.core.dep import get_current_user
from fastapi import Form
from app.model.models import Tournament, TournamentCreate
from app.utils.helpers import database_dependency
from app.services.supabase import supabase
from app.utils.helpers import upload_to_supabase
from app.cruds.tournaments import (
    get_tournament,
    get_tournaments,
    update_tournament,
    delete_tournament,
    create_tournament,
)

router = APIRouter(prefix="/tournament", tags=["Tournaments"])


@router.get("/", response_model=List[Tournament])
def read_tournaments(db: database_dependency, skip: int = 0, limit: int = 100):
    return get_tournaments(db=db, skip=skip, limit=limit)


@router.get("/{tournement_id}", response_model=Tournament)
def read_tournament(tournament_id: uuid.UUID, db: database_dependency):
    tournamet = get_tournament(db=db, tournament_id=tournament_id)
    if not tournamet:
        raise HTTPException(detail="Not Found!!", status_code=status.HTTP_404_NOT_FOUND)
    return tournamet


@router.post("/upload")
async def upload_logo(
    db: database_dependency,
    file: UploadFile = File(...),
    tournament_id: uuid.UUID = Form(...),
):
    url = await upload_to_supabase(file, "tournaments")
    update_tournament(
        db=db, tournament_id=tournament_id, tournament_data={"logo_url": url}
    )
    return {"tournament_id": tournament_id, "logo_url": url}


@router.post("/", response_model=Tournament)
async def add_tournament(
    tournament: TournamentCreate,
    db: database_dependency,
    user=Depends(get_current_user),
):
    return create_tournament(db=db, tournament=tournament)


@router.put("/{tournament_id}", response_model=Tournament)
def put_tournament(
    tournament_id: uuid.UUID,
    tournamet_data: dict,
    db: database_dependency,
    user=Depends(get_current_user),
):
    updated = update_tournament(
        db=db, tournament_id=tournament_id, tournament_data=tournamet_data
    )
    if not updated:
        raise HTTPException(detail="Not Found!!", status_code=status.HTTP_404_NOT_FOUND)
    return updated


@router.delete("/{tournament_id}", response_model=dict)
def remove_tournament(
    tournament_id: uuid.UUID, db: database_dependency, user=Depends(get_current_user)
):
    removed = delete_tournament(db=db, tournament_id=tournament_id)
    if not removed:
        raise HTTPException(detail="Not Found!!", status_code=status.HTTP_404_NOT_FOUND)
    return {"ok": True}
