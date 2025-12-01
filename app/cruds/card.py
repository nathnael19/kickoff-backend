from typing import List, Optional
from app.model.models import Card
from sqlmodel import Session, select
from app.utils.helpers import add_to_db, delete_from_db, update_to_db
import uuid


def get_card(db: Session, card_id: uuid.UUID):
    return db.get(Card, card_id)


def get_cards(db: Session, skip: int = 0, limit: int = 0) -> List[Card]:
    statement = select(Card).offset(skip).limit(limit)
    return list(db.exec(statement).all())


def create_card(db: Session, card: Card):
    return add_to_db(db, card)


def update_card(db: Session, card_data: dict, card_id: uuid.UUID) -> Optional[Card]:
    return update_to_db(db, card_id, card_data, Card)


def delete_card(db: Session, card_id: uuid.UUID) -> bool:
    return delete_from_db(db, card_id, Card)
