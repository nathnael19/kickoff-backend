from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship
import uuid
from datetime import datetime
from enum import Enum

# ---------------- Enums ---------------- #


class TournamentStatus(str, Enum):
    planned = "planned"
    ongoing = "ongoing"
    finished = "finished"


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


class MatchEventType(str, Enum):
    yellow_card = "Yellow Card"
    red_card = "Red Card"
    goal = "Goal"
    penalty = "Penalty"


class CardType(str, Enum):
    yellow = "Yellow"
    red = "Red"


# ---------------- Models ---------------- #


# --- Tournament ---
class TournamentBase(SQLModel):
    name: str = Field(..., max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    status: TournamentStatus = Field(default=TournamentStatus.planned)
    logo_url: Optional[str] = None
    start_date: datetime
    end_date: Optional[datetime] = None


class TournamentCreate(TournamentBase):
    pass


class Tournament(TournamentBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    teams: List["Team"] = Relationship(back_populates="tournament")
    matches: List["Match"] = Relationship(back_populates="tournament")
    standings: List["Standing"] = Relationship(back_populates="tournament")


# --- Team ---
class TeamBase(SQLModel):
    # Foreign keys must be in Base/Create so you can link them on creation
    tournament_id: uuid.UUID = Field(foreign_key="tournament.id", ondelete="CASCADE")
    name: str = Field(..., max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    department: str = Field(..., max_length=100)
    coach: str = Field(..., max_length=100)
    logo_url: Optional[str] = None


class TeamCreate(TeamBase):
    pass


class Team(TeamBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    tournament: Optional[Tournament] = Relationship(back_populates="teams")
    players: List["Player"] = Relationship(back_populates="team")

    home_matches: List["Match"] = Relationship(
        back_populates="home_team",
        sa_relationship_kwargs={"foreign_keys": "[Match.home_team_id]"},
    )
    away_matches: List["Match"] = Relationship(
        back_populates="away_team",
        sa_relationship_kwargs={"foreign_keys": "[Match.away_team_id]"},
    )
    goals: List["Goal"] = Relationship(back_populates="team")
    card: List["Card"] = Relationship(back_populates="team")
    standings: List["Standing"] = Relationship(back_populates="team")


# --- Player ---
class PlayerBase(SQLModel):
    team_id: uuid.UUID = Field(foreign_key="team.id", ondelete="CASCADE")
    name: str = Field(max_length=100)
    position: PlayerPosition
    number: int = Field(ge=1, le=99)
    photo_url: str


class PlayerCreate(PlayerBase):
    pass


class Player(PlayerBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    team: Optional[Team] = Relationship(back_populates="players")
    matchevent: List["MatchEvent"] = Relationship(back_populates="player")
    card: List["Card"] = Relationship(back_populates="player")


# --- Match ---
class MatchBase(SQLModel):
    tournament_id: uuid.UUID = Field(foreign_key="tournament.id", ondelete="CASCADE")
    home_team_id: uuid.UUID = Field(foreign_key="team.id", ondelete="CASCADE")
    away_team_id: uuid.UUID = Field(foreign_key="team.id", ondelete="CASCADE")
    home_score: int = Field(default=0)
    away_score: int = Field(default=0)
    match_date: datetime
    status: TournamentStatus = Field(default=TournamentStatus.planned)
    location: str = Field(max_length=100)
    referee: str = Field(max_length=100)


class MatchCreate(MatchBase):
    pass


class Match(MatchBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    tournament: Optional[Tournament] = Relationship(back_populates="matches")
    home_team: Optional[Team] = Relationship(
        back_populates="home_matches",
        sa_relationship_kwargs={"foreign_keys": "[Match.home_team_id]"},
    )
    away_team: Optional[Team] = Relationship(
        back_populates="away_matches",
        sa_relationship_kwargs={"foreign_keys": "[Match.away_team_id]"},
    )
    goals: List["Goal"] = Relationship(back_populates="match")
    matchevent: List["MatchEvent"] = Relationship(back_populates="match")
    lineups: List["MatchLineup"] = Relationship(back_populates="match")
    card: List["Card"] = Relationship(back_populates="match")


# --- Goal ---
class GoalBase(SQLModel):
    match_id: uuid.UUID = Field(foreign_key="match.id", ondelete="CASCADE")
    team_id: uuid.UUID = Field(foreign_key="team.id", ondelete="CASCADE")
    scorer_player_id: uuid.UUID = Field(foreign_key="player.id", ondelete="CASCADE")
    # Note: If an assist is optional, you might want to make this Optional[uuid.UUID] = None
    assist_player_id: uuid.UUID = Field(foreign_key="player.id", ondelete="CASCADE")
    minutes: int = Field(ge=0, le=120)


class GoalCreate(GoalBase):
    pass


class Goal(GoalBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    match: Optional[Match] = Relationship(back_populates="goals")
    team: Optional[Team] = Relationship(back_populates="goals")
    scorer: Optional[Player] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[Goal.scorer_player_id]"}
    )
    assist: Optional[Player] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[Goal.assist_player_id]"}
    )


# --- MatchEvent ---
class MatchEventBase(SQLModel):
    match_id: uuid.UUID = Field(foreign_key="match.id", ondelete="CASCADE")
    player_id: uuid.UUID = Field(foreign_key="player.id", ondelete="CASCADE")
    event_type: MatchEventType
    minute: int = Field(ge=0, le=120)


class MatchEventCreate(MatchEventBase):
    pass


class MatchEvent(MatchEventBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    match: Optional[Match] = Relationship(back_populates="matchevent")
    player: Optional[Player] = Relationship(back_populates="matchevent")


# --- MatchLineup ---
class MatchLineupBase(SQLModel):
    match_id: uuid.UUID = Field(foreign_key="match.id", ondelete="CASCADE")
    team_id: uuid.UUID = Field(foreign_key="team.id", ondelete="CASCADE")
    player_id: uuid.UUID = Field(foreign_key="player.id", ondelete="CASCADE")


class MatchLineupCreate(MatchLineupBase):
    pass


class MatchLineup(MatchLineupBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)

    match: Optional[Match] = Relationship(back_populates="lineups")
    team: Optional[Team] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[MatchLineup.team_id]"}
    )
    player: Optional[Player] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[MatchLineup.player_id]"}
    )


# --- Card ---
class CardBase(SQLModel):
    match_id: uuid.UUID = Field(foreign_key="match.id", ondelete="CASCADE")
    player_id: uuid.UUID = Field(foreign_key="player.id", ondelete="CASCADE")
    team_id: uuid.UUID = Field(foreign_key="team.id", ondelete="CASCADE")
    card_type: CardType
    minute: int = Field(ge=0, le=120)


class CardCreate(CardBase):
    pass


class Card(CardBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)

    match: Optional[Match] = Relationship(back_populates="card")
    player: Optional[Player] = Relationship(back_populates="card")
    team: Optional[Team] = Relationship(back_populates="card")


# --- Standing ---
class StandingBase(SQLModel):
    tournament_id: uuid.UUID = Field(foreign_key="tournament.id", ondelete="CASCADE")
    team_id: uuid.UUID = Field(foreign_key="team.id", ondelete="CASCADE")
    match_played: int = Field(default=0, ge=0)
    wins: int = Field(default=0, ge=0)
    draws: int = Field(default=0, ge=0)
    loss: int = Field(default=0, ge=0)
    points: int = Field(default=0, ge=0)


class StandingCreate(StandingBase):
    pass


class Standing(StandingBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    updated_at: datetime = Field(default_factory=datetime.now)

    team: Optional[Team] = Relationship(back_populates="standings")
    tournament: Optional[Tournament] = Relationship(back_populates="standings")
