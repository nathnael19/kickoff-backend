from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.model.models import Player, PlayerCreate
import uuid
from app.core.dep import get_current_user
from app.utils.helpers import database_dependency
from app.cruds.player import (
    create_player,
    get_player,
    get_players,
    update_player,
    delete_player,
)

router = APIRouter(prefix="/players", tags=["Players"])


@router.get("/", response_model=List[Player])
def read_players(db: database_dependency, skip: int = 0, limit: int = 100):
    return get_players(db=db, skip=skip, limit=limit)


@router.get("/{player_id}", response_model=Player)
def read_player(player_id: uuid.UUID, db: database_dependency):
    player = get_player(db=db, player_id=player_id)
    if not player:
        raise HTTPException(detail="Not found!", status_code=status.HTTP_404_NOT_FOUND)
    return player


@router.post("/", response_model=Player)
def add_player(
    player: PlayerCreate, db: database_dependency, user=Depends(get_current_user)
):
    return create_player(db=db, player=player)


@router.put("/", response_model=Player)
def put_player(
    player_id: uuid.UUID,
    player_data: dict,
    db: database_dependency,
    user=Depends(get_current_user),
):
    update = update_player(db=db, player_id=player_id, player_data=player_data)
    if not update:
        raise HTTPException(detail="Not Found!!", status_code=status.HTTP_404_NOT_FOUND)
    return update


@router.delete("/", response_model=dict)
def remove_player(
    player_id: uuid.UUID, db: database_dependency, user=Depends(get_current_user)
):
    delete = delete_player(db=db, player_id=player_id)
    if not delete:
        raise HTTPException(detail="Not Found!!", status_code=status.HTTP_404_NOT_FOUND)
    return {"ok": True}
