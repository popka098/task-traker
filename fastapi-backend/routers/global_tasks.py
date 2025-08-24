from fastapi import APIRouter, Depends, HTTPException

from sqlmodel import Session, select
from database import get_session

from models.global_task import GlobalTask, GlobalTaskCreate, GlobalTaskRead

from typing import Annotated

SessionDep = Annotated[Session, Depends(get_session)]

router = APIRouter(prefix="/api/globaltasks", tags=["GlobalTasks"])

@router.post("/", response_model=GlobalTaskCreate)
def create_global_task(task: GlobalTaskCreate, session: SessionDep) -> GlobalTask:
    new_task = GlobalTask.model_validate(task)
    session.add(new_task)
    session.commit()
    session.refresh(new_task)
    return task

@router.get("/", response_model=list[GlobalTaskRead])
def read_global_tasks(session: SessionDep) -> list[GlobalTaskRead]:
    global_tasks = session.exec(select(GlobalTask)).all()
    return global_tasks

@router.get("/{id}", response_model=GlobalTaskRead)
def read_global_task(id: int, session: SessionDep) -> GlobalTaskRead:
    task = session.get(GlobalTask, id)
    if not task:
        raise HTTPException(404, "Global Task not found")
    return task