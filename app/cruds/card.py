from typing import List, Optional
from app.model.models import Card
from sqlmodel import Session, select
import uuid


def get_card(db: Session, card_id: uuid.UUID):
    return db.get(Card, card_id)


def get_cards(db: Session, skip: int = 0, limit: int = 0) -> List[Card]:
    statement = select(Card).offset(skip).limit(limit)
    return list(db.exec(statement).all())


def create_card(db: Session, card: Card) -> Card:
    db.add(card)
    db.commit()
    db.refresh(card)
    return card


def update_card(db: Session, card_data: dict, card_id: uuid.UUID) -> Optional[Card]:
    card = db.get(Card, card_id)
    if not card:
        return None
    for key, value in card_data.items():
        setattr(card, key, value)
    db.add(card)
    db.commit()
    db.refresh(card)

    return card


def delete_card(db: Session, card_id: uuid.UUID) -> bool:
    card = db.get(Card, card_id)
    if not card:
        return False
    db.delete(card)
    db.commit()
    return True
