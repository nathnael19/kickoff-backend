from fastapi import FastAPI, Depends, HTTPException

from app.services.supabase import login
from .database.db import create_db_and_tables
from app.core.dep import get_current_user
from pydantic import EmailStr
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


@app.post("/login")
def login_route(email: str, password: str):
    token = login(email, password)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"access_token": token, "token_type": "bearer"}


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
def home(user=Depends(get_current_user)):
    return {"message": "homepage"}
