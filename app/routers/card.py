from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List, Optional
from app.database.db import get_session
from app.model.models import Card
import uuid
from app.cruds.card import create_card, get_card, get_cards, update_card, delete_card

router = APIRouter(prefix="/cards", tags=["Cards"])


@router.get("/", response_model=List[Card])
def read_cards(db: Session = Depends(get_session), skip: int = 0, limit: int = 100):
    return get_cards(db=db, skip=skip, limit=limit)


@router.get("/{card_id}", response_model=Card)
def read_card(card_id: uuid.UUID, db: Session = Depends(get_session)):
    card = get_card(db=db, card_id=card_id)
    if not card:
        raise HTTPException(detail="Not found!", status_code=status.HTTP_404_NOT_FOUND)
    return card


@router.post("/", response_model=Card)
def add_card(card: Card, db: Session = Depends(get_session)):
    return create_card(db=db, card=card)


@router.put("/", response_model=Card)
def put_card(card_id: uuid.UUID, card_data: dict, db: Session = Depends(get_session)):
    update = update_card(db=db, card_id=card_id, card_data=card_data)
    if not update:
        raise HTTPException(detail="Not Found!!", status_code=status.HTTP_404_NOT_FOUND)
    return update


@router.delete("/", response_model=dict)
def remove_card(card_id: uuid.UUID, db: Session = Depends(get_session)):
    delete = delete_card(db=db, card_id=card_id)
    if not delete:
        raise HTTPException(detail="Not Found!!", status_code=status.HTTP_404_NOT_FOUND)
    return {"ok": True}
