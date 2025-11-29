from enum import Enum
from sqlmodel import SQLModel, Field
from typing import Optional
import uuid
from datetime import datetime


class TournamentStatus(str, Enum):
    planned = "planned"
    ongoing = "ongoing"
    finished = "finished"


class Tournament(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str
    description: str = Field(max_length=500)
    status: TournamentStatus
    logo_url: Optional[str] = None
    start_date: datetime
    end_date: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
