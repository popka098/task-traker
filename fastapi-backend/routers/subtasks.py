from fastapi import APIRouter, Depends, HTTPException

from sqlmodel import Session
from database import get_session

from models.subtask import SubTask, SubTaskCreate, SubTaskUpdate, SubTaskRead

from typing import Annotated

SessionDep = Annotated[Session, Depends(get_session)]

router = APIRouter(prefix="/api/subtasks", tags=["SubTasks", "Tasks"])

@router.post("/", response_model=SubTaskCreate)
def create_subtask(task: SubTaskCreate, session: SessionDep) -> SubTask:
    new_task = SubTask.model_validate(task)
    session.add(new_task)
    session.commit()
    session.refresh(new_task)
    return task