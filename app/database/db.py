from sqlmodel import SQLModel, create_engine, Session
from app.core.config import settings

# Engine
engine = create_engine(
    settings.online_url,
    echo=True,
)


# Create tables
def create_db_and_tables():
    from app.model.models import (
        Card,
        Goal,
        Match,
        MatchEvent,
        MatchLineup,
        Standing,
        Player,
        Team,
        Tournament,
    )

    SQLModel.metadata.create_all(engine)


def get_session():
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()
