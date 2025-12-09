from fastapi import FastAPI, Depends, HTTPException, Request, status
from pydantic import BaseModel, EmailStr

from app.services.supabase import login
from .database.db import create_db_and_tables
from app.core.dep import get_current_user
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

from slowapi import Limiter
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# -------------------------------
# FastAPI app and rate limiter
# -------------------------------
app = FastAPI(title="Kick OFF", version="1.0.0")


origins = [
    "http://localhost:8100",  # Flutter Web local
    "http://127.0.0.1:8100",
    "your-flutter-app-domain.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)


# Custom rate limit exception handler
@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        content={"detail": "Too many requests. Please try again later."},
    )


# -------------------------------
# Pydantic login request model
# -------------------------------
class LoginRequest(BaseModel):
    email: EmailStr
    password: str


# -------------------------------
# Rate-limited login route
# -------------------------------
@app.post("/login")
@limiter.limit("3/minute")
async def login_route(request: Request, data: LoginRequest):
    try:
        token = login(data.email, data.password)
        if not token:
            # This will properly return 401 to the user
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
            )
        return {"access_token": token, "token_type": "bearer"}

    except HTTPException:
        # Re-raise so FastAPI handles it properly
        raise
    except Exception as e:
        # Catch any unexpected errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@app.post("/logout")
async def logout(current_user: dict = Depends(get_current_user)):
    return {"message": "Logged out successfully"}


# -------------------------------
# Include routers
# -------------------------------
app.include_router(tournaments.router)
app.include_router(team.router)
app.include_router(standing.router)
app.include_router(player.router)
app.include_router(match.router)
app.include_router(match_lineup.router)
app.include_router(match_event.router)
app.include_router(goals.router)
app.include_router(card.router)


# -------------------------------
# Database startup
# -------------------------------
@app.on_event("startup")
def on_startup():
    create_db_and_tables()


# -------------------------------
# Home route (protected)
# -------------------------------
@app.get("/")
def home():
    return {"message": "homepage"}
