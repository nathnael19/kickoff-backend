from typing import Annotated

from fastapi import Depends
from typing import Any
from sqlmodel import Session
from app.database.db import get_session


database_dependency = Annotated[Session, Depends(get_session)]


def add_to_db(db: Session, model: Any):
    db.add(model)
    db.commit()
    db.refresh(model)
    return model
