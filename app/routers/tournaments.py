from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List
import uuid
from app.model.models import Tournament
from app.database.db import get_session
from app.cruds.tournaments import (
    get_tournament,
    get_tournaments,
    update_tournament,
    delete_tournament,
    create_tournament,
)

router = APIRouter(prefix="/tournament", tags=["Tournaments"])


@router.get("/", response_model=List[Tournament])
def read_tournaments(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_session)
):
    return get_tournaments(db=db, skip=skip, limit=limit)


@router.get("/{tournement_id}", response_model=Tournament)
def read_tournament(tournament_id: uuid.UUID, db: Session = Depends(get_session)):
    tournamet = get_tournament(db=db, tournament_id=tournament_id)
    if not tournamet:
        raise HTTPException(detail="Not Found!!", status_code=status.HTTP_404_NOT_FOUND)
    return tournamet


@router.post("/", response_model=Tournament)
def add_tournament(tournamet: Tournament, db: Session = Depends(get_session)):
    return create_tournament(db=db, tournament=tournamet)


@router.put("/{tournament_id}", response_model=Tournament)
def put_tournament(
    tournament_id: uuid.UUID, tournamet_data: dict, db: Session = Depends(get_session)
):
    updated = update_tournament(
        db=db, tournament_id=tournament_id, tournament_data=tournamet_data
    )
    if not updated:
        raise HTTPException(detail="Not Found!!", status_code=status.HTTP_404_NOT_FOUND)
    return updated


@router.delete("/{tournament_id}", response_model=dict)
def remove_tournament(tournament_id: uuid.UUID, db: Session = Depends(get_session)):
    removed = delete_tournament(db=db, tournament_id=tournament_id)
    if not removed:
        raise HTTPException(detail="Not Found!!", status_code=status.HTTP_404_NOT_FOUND)
    return {"ok": True}
