from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List, Optional
from app.database.db import get_session
from app.model.models import Goal
import uuid
from app.cruds.goals import create_goal, get_goal, get_goals, update_goal, delete_goal

router = APIRouter(prefix="/goals", tags=["Goals"])


@router.get("/", response_model=List[Goal])
def read_goals(db: Session = Depends(get_session), skip: int = 0, limit: int = 100):
    return get_goals(db=db, skip=skip, limit=limit)


@router.get("/{goal_id}", response_model=Goal)
def read_goal(goal_id: uuid.UUID, db: Session = Depends(get_session)):
    goal = get_goal(db=db, goal_id=goal_id)
    if not goal:
        raise HTTPException(detail="Not found!", status_code=status.HTTP_404_NOT_FOUND)
    return goal


@router.post("/", response_model=Goal)
def add_goal(goal: Goal, db: Session = Depends(get_session)):
    return create_goal(db=db, goal=goal)


@router.put("/", response_model=Goal)
def put_goal(goal_id: uuid.UUID, goal_data: dict, db: Session = Depends(get_session)):
    update = update_goal(db=db, goal_id=goal_id, goal_data=goal_data)
    if not update:
        raise HTTPException(detail="Not Found!!", status_code=status.HTTP_404_NOT_FOUND)
    return update


@router.delete("/", response_model=dict)
def remove_goal(goal_id: uuid.UUID, db: Session = Depends(get_session)):
    delete = delete_goal(db=db, goal_id=goal_id)
    if not delete:
        raise HTTPException(detail="Not Found!!", status_code=status.HTTP_404_NOT_FOUND)
    return {"ok": True}
