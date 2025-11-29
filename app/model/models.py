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

    # One tournament → many teams
    teams: List["Team"] = Relationship(back_populates="tournament")

    # One tournament → many matches
    matches: List["Match"] = Relationship(back_populates="tournament")


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

    # Many teams → one tournament
    tournament: Optional[Tournament] = Relationship(back_populates="teams")

    # One team → many players
    players: List["Player"] = Relationship(back_populates="team")

    # One team → many home matches
    home_matches: List["Match"] = Relationship(back_populates="home_team")

    # One team → many away matches
    away_matches: List["Match"] = Relationship(back_populates="away_team")


class PlayerPosition(str, Enum):
    gk = "GK"
    cd = "CD"
    lb = "LB"
    rb = "RB"
    cm = "CM"
    cdm = "CDM"
    cam = "CAM"
    lw = "LW"
    rw = "RW"
    cf = "CF"


class Player(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    team_id: uuid.UUID = Field(foreign_key="team.id")
    name: str = Field(max_length=100)
    position: PlayerPosition
    number: int = Field(ge=1, le=99)
    photo_url: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Many players → one team
    team: Optional["Team"] = Relationship(back_populates="players")


class Match(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    tournament_id: uuid.UUID = Field(foreign_key="tournament.id")
    home_team_id: uuid.UUID = Field(foreign_key="team.id")
    away_team_id: uuid.UUID = Field(foreign_key="team.id")

    home_score: int = Field(default=0)
    away_score: int = Field(default=0)
    match_date: datetime
    status: TournamentStatus = Field(default=TournamentStatus.planned)
    location: str = Field(max_length=100)
    referee: str = Field(max_length=100)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Many matches → one tournament
    tournament: Optional["Tournament"] = Relationship(back_populates="matches")

    # Match → home team
    home_team: Optional["Team"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[Match.home_team_id]"},
        back_populates="home_matches",
    )

    # Match → away team
    away_team: Optional["Team"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[Match.away_team_id]"},
        back_populates="away_matches",
    )
