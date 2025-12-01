from fastapi import FastAPI
from .database.db import create_db_and_tables
from app.routers import (
    tournaments,
    team,
    standing,
    player,
    match,
    match_lineup,
    match_event,
    goals,
    card,
)

app = FastAPI(title="Kick OFF", version="1.0.0")

app.include_router(tournaments.router)
app.include_router(team.router)
app.include_router(standing.router)
app.include_router(player.router)
app.include_router(match.router)
app.include_router(match_lineup.router)
app.include_router(match_event.router)
app.include_router(goals.router)
app.include_router(card.router)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
def home():
    return {"message": "homepage"}
