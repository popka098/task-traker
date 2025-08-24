from fastapi import APIRouter, Depends, HTTPException

from sqlmodel import Session
from database import get_session

from models.global_task import GlobalTask, GlobalTaskRead
from models.subtask import SubTask, SubTaskRead

from typing import Annotated

SessionDep = Annotated[Session, Depends(get_session)]

router = APIRouter(prefix="/api/globaltasks", tags=["GlobalTasks SubTasks"])

@router.get("/{id}/subtasks", response_model=list[SubTaskRead])
def get_subtasks_by_globaltaks(id: int, session: SessionDep) -> list[SubTaskRead]:
    global_task = session.get(GlobalTask, id)
    if not global_task:
        raise HTTPException(404, "GlobalTask not found")

    return global_task.subtasks