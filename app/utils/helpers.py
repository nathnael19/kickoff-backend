from typing import Annotated, Type
import uuid

from fastapi import Depends
from typing import Any
from sqlmodel import SQLModel, Session
from app.database.db import get_session


database_dependency = Annotated[Session, Depends(get_session)]


def add_to_db(db: Session, model: Any):
    db.add(model)
    db.commit()
    db.refresh(model)
    return model


def delete_from_db(db: Session, id: uuid.UUID, model: Type[SQLModel]) -> bool:
    delete = db.get(model, id)
    if not delete:
        return False
    db.delete(delete)
    db.commit()
    return True
