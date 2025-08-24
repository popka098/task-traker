from fastapi import APIRouter, Depends, HTTPException

from sqlmodel import Session
from database import get_session

from models.user import User
from models.subtask import SubTask, SubTaskRead, SubTaskCreate

from typing import Annotated

SessionDep = Annotated[Session, Depends(get_session)]

router = APIRouter(prefix="/api/users", tags=["Users Subtasks"])

@router.get("/{id}/subtasks", response_model=list[SubTaskRead])
def read_global_tasks_by_user(id: int, session: SessionDep) -> list[SubTaskRead]:
    user = session.get(User, id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user.subtasks