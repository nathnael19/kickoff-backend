from fastapi import FastAPI
from .database.db import create_db_and_tables
from app.routers import tournaments

app = FastAPI(title="Kick OFF")

app.include_router(tournaments.router)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
def home():
    return {"message": "homepage"}
