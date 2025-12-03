from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import uuid


class PlayerRead(BaseModel):
    id: uuid.UUID
    name: str
    position: str
    number: int
    photo_url: str

    class Config:
        from_attributes = True


class TeamRead(BaseModel):
    id: uuid.UUID
    name: str
    description: Optional[str]
    department: str
    coach: str
    logo_url: Optional[str]
    players: List[PlayerRead] = []

    class Config:
        from_attributes = True


class TournamentRead(BaseModel):
    id: uuid.UUID
    name: str
    description: Optional[str]
    status: str
    logo_url: Optional[str]
    start_date: datetime
    end_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    teams: List[TeamRead] = []

    class Config:
        from_attributes = True
