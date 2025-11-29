from sqlmodel import create_engine, SQLModel
from app.core.config import settings


engine = create_engine(settings.postgres_url, echo=True)


def create_tables():
    SQLModel.metadata.create_all(engine)
