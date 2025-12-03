from typing import Annotated, Type
import uuid
from fastapi import Depends, HTTPException, status
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


def update_to_db(db: Session, id: uuid.UUID, data: dict, model: Type[SQLModel]):
    update = db.get(model, id)
    if not update:
        return None
    for key, value in data.items():
        setattr(update, key, value)
    return add_to_db(db, update)


raised_error = HTTPException(
    detail="Not Found!!", status_code=status.HTTP_404_NOT_FOUND
)


import uuid
from fastapi import UploadFile, HTTPException
from app.services.supabase import supabase


async def upload_to_supabase(file: UploadFile, bucket: str) -> str:
    file_bytes = await file.read()
    filename = f"{uuid.uuid4()}_{file.filename}"

    res = supabase.storage.from_(bucket).upload(filename, file_bytes, {"upsert": "true"})  # type: ignore
    error = None

    if isinstance(res, dict):
        error = res.get("error")
    else:
        error = getattr(res, "error", None)

    if error:
        message = error.get("message") if isinstance(error, dict) else str(error)
        raise HTTPException(400, message)

    return supabase.storage.from_(bucket).get_public_url(filename)
