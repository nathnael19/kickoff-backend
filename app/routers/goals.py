from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.model.models import Goal, GoalCreate
import uuid
from app.utils.helpers import database_dependency
from app.cruds.goals import create_goal, get_goal, get_goals, update_goal, delete_goal

router = APIRouter(prefix="/goals", tags=["Goals"])


@router.get("/", response_model=List[Goal])
def read_goals(db: database_dependency, skip: int = 0, limit: int = 100):
    return get_goals(db=db, skip=skip, limit=limit)


@router.get("/{goal_id}", response_model=Goal)
def read_goal(goal_id: uuid.UUID, db: database_dependency):
    goal = get_goal(db=db, goal_id=goal_id)
    if not goal:
        raise HTTPException(detail="Not found!", status_code=status.HTTP_404_NOT_FOUND)
    return goal


@router.post("/", response_model=Goal)
def add_goal(goal: GoalCreate, db: database_dependency):
    return create_goal(db=db, goal=goal)


@router.put("/", response_model=Goal)
def put_goal(goal_id: uuid.UUID, goal_data: dict, db: database_dependency):
    update = update_goal(db=db, goal_id=goal_id, goal_data=goal_data)
    if not update:
        raise HTTPException(detail="Not Found!!", status_code=status.HTTP_404_NOT_FOUND)
    return update


@router.delete("/", response_model=dict)
def remove_goal(goal_id: uuid.UUID, db: database_dependency):
    delete = delete_goal(db=db, goal_id=goal_id)
    if not delete:
        raise HTTPException(detail="Not Found!!", status_code=status.HTTP_404_NOT_FOUND)
    return {"ok": True}
