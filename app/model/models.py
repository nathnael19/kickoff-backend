from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship
import uuid
from datetime import datetime
from enum import Enum


class TournamentStatus(str, Enum):
    planned = "planned"
    ongoing = "ongoing"
    finished = "finished"


class Tournament(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(..., max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    status: TournamentStatus = Field(default=TournamentStatus.planned)
    logo_url: Optional[str] = None
    start_date: datetime
    end_date: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # ORM-style relationship
    teams: List["Team"] = Relationship(back_populates="tournament")


class Team(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    tournament_id: uuid.UUID = Field(foreign_key="tournament.id")
    name: str = Field(..., max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    department: str = Field(..., max_length=100)
    coach: str = Field(..., max_length=100)
    logo_url: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # ORM-style relationship
    tournament: Optional[Tournament] = Relationship(back_populates="teams")
