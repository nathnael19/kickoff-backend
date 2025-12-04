from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from pydantic import BaseModel
import uuid
from app.cruds.player import get_player
from app.model.models import MatchLineup, MatchLineupCreate, Player
from app.core.dep import get_current_user
from app.utils.helpers import database_dependency
from app.cruds.match_lineup import (
    create_match_lineup,
    get_match_lineup,
    get_match_lineups,
    update_match_lineup,
    delete_match_lineup,
)

router = APIRouter(prefix="/match_lineups", tags=["Match Lineups"])


# ---------------- Pydantic model for adding players ---------------- #
class LineupAddPlayers(BaseModel):
    player_ids: List[uuid.UUID]


# ---------------- CRUD Endpoints ---------------- #


@router.get("/", response_model=List[MatchLineup])
def read_match_lineups(db: database_dependency, skip: int = 0, limit: int = 100):
    return get_match_lineups(db=db, skip=skip, limit=limit)


@router.get("/{match_lineup_id}", response_model=MatchLineup)
def read_match_lineup(match_lineup_id: uuid.UUID, db: database_dependency):
    match_lineup = get_match_lineup(db=db, match_lineup_id=match_lineup_id)
    if not match_lineup:
        raise HTTPException(detail="Not found!", status_code=status.HTTP_404_NOT_FOUND)
    return match_lineup


@router.post("/", response_model=MatchLineup)
def add_match_lineup(
    match_lineup: MatchLineupCreate,
    db: database_dependency,
    user=Depends(get_current_user),
):
    return create_match_lineup(db=db, match_lineup=match_lineup)


@router.post("/add_players/{match_id}/{team_id}", response_model=MatchLineup)
def add_players_to_lineup(
    match_id: uuid.UUID,
    team_id: uuid.UUID,
    payload: LineupAddPlayers,
    db: database_dependency,
    user=Depends(get_current_user),
):
    # Check if lineup exists for this match and team
    lineup = get_match_lineups(db=db, skip=0, limit=100)
    lineup = next(
        (l for l in lineup if l.match_id == match_id and l.team_id == team_id), None
    )

    if not lineup:
        # Create new lineup row if not exists
        match_lineup = MatchLineupCreate(
            match_id=match_id, team_id=team_id, player_ids=payload.player_ids
        )
        return create_match_lineup(db=db, match_lineup=match_lineup)
    else:
        # Append new players, avoiding duplicates
        existing_ids = set(lineup.player_ids)
        new_ids = [p for p in payload.player_ids if p not in existing_ids]
        lineup.player_ids.extend(new_ids)
        updated = update_match_lineup(
            db=db,
            match_lineup_id=lineup.id,
            match_lineup_data={"player_ids": lineup.player_ids},
        )
        return updated


@router.put("/", response_model=MatchLineup)
def put_match_lineup(
    match_lineup_id: uuid.UUID,
    match_lineup_data: dict,
    db: database_dependency,
    user=Depends(get_current_user),
):
    update = update_match_lineup(
        db=db, match_lineup_id=match_lineup_id, match_lineup_data=match_lineup_data
    )
    if not update:
        raise HTTPException(detail="Not Found!!", status_code=status.HTTP_404_NOT_FOUND)
    return update


@router.delete("/", response_model=dict)
def remove_match_lineup(
    match_lineup_id: uuid.UUID, db: database_dependency, user=Depends(get_current_user)
):
    delete = delete_match_lineup(db=db, match_lineup_id=match_lineup_id)
    if not delete:
        raise HTTPException(detail="Not Found!!", status_code=status.HTTP_404_NOT_FOUND)
    return {"ok": True}


@router.get("/players/{match_id}/{team_id}", response_model=List[Player])
def get_lineup_players(
    match_id: uuid.UUID,
    team_id: uuid.UUID,
    db: database_dependency,
    user=Depends(get_current_user),
):
    # Get all lineups for this match and team
    lineups = get_match_lineups(db=db, skip=0, limit=100)
    lineup = next(
        (l for l in lineups if l.match_id == match_id and l.team_id == team_id), None
    )

    if not lineup:
        raise HTTPException(
            status_code=404, detail="Lineup not found for this match/team"
        )

    # Assuming your MatchLineup model stores a list of player IDs
    player_ids = getattr(lineup, "player_ids", [])

    # Fetch Player objects
    players = [get_player(db=db, player_id=p_id) for p_id in player_ids]

    return players
