from fastapi import APIRouter, Depends, HTTPException

from sqlmodel import Session, select
from database import get_session

from models.subtask import SubTask, SubTaskCreate, SubTaskUpdate, SubTaskRead
from models.global_task import GlobalTask

from typing import Annotated

SessionDep = Annotated[Session, Depends(get_session)]

router = APIRouter(prefix="/api/subtasks", tags=["SubTasks", "Tasks"])

@router.post("/", response_model=SubTaskRead)
def create_subtask(task: SubTaskCreate, session: SessionDep) -> SubTaskRead:
    new_task = SubTask.model_validate(task)
    session.add(new_task)
    session.commit()
    session.refresh(new_task)
    return new_task

@router.get("/", response_model=list[SubTaskRead])
def read_global_tasks(session: SessionDep) -> list[SubTaskRead]:
    subtasks = session.exec(select(SubTask)).all()
    return subtasks

@router.get("/{id}", response_model=SubTaskRead)
def read_global_task(id: int, session: SessionDep) -> SubTaskRead:
    task = session.get(SubTask, id)
    if not task:
        raise HTTPException(404, "SubTask not found")
    return task

@router.delete("/{id}")
def delete_global_task(id:int, session: SessionDep):
    subtask = session.get(SubTask, id)
    if not subtask:
        raise HTTPException(404, "SubTask not found")

    session.delete(subtask)
    session.commit()
    return {"ok": True}

@router.patch("/{id}")
def update_global_task(id:int, session:SessionDep, new_task: SubTaskUpdate) -> SubTask:
    subtask = session.get(SubTask, id)
    if not subtask:
        raise HTTPException(404, "SubTask not found")

    task_data = new_task.model_dump(exclude_unset=True)
    for key, value in task_data.items():
        setattr(subtask, key, value)

    session.add(subtask)
    session.commit()
    session.refresh(subtask)
    return subtask

@router.patch("/{id}/complete")
def complete_subtask(id: int, session:SessionDep):
    subtask = session.get(SubTask, id)
    if not subtask:
        raise HTTPException(404, "SubTask not found")
    subtask.is_completed = True
    session.add(subtask)

    tasks = session.exec(
        select(SubTask).where(SubTask.global_task_id == subtask.global_task_id)
    ).all()
    if all(t.is_completed for t in tasks):
        global_task = session.get(GlobalTask, subtask.global_task_id)
        global_task.is_completed = True
        session.add(global_task)

    session.commit()
    session.refresh(subtask)
    return subtask