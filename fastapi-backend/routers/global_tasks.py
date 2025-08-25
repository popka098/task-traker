from fastapi import APIRouter, Depends, HTTPException

from sqlmodel import Session, select
from database import get_session

from models.global_task import GlobalTask, GlobalTaskCreate, GlobalTaskRead, GlobalTaskUpdate
from models.many_to_many_links.global_task_user_link import GlobalTaskUserLink

from typing import Annotated

SessionDep = Annotated[Session, Depends(get_session)]

router = APIRouter(prefix="/api/globaltasks", tags=["GlobalTasks", "Tasks"])

@router.post("/", response_model=GlobalTaskCreate)
def create_global_task(task: GlobalTaskCreate, session: SessionDep) -> GlobalTask:
    new_task = GlobalTask.model_validate(task)
    session.add(new_task)
    session.commit()
    session.refresh(new_task)

    link = GlobalTaskUserLink(user_id=new_task.resp_id, global_task_id=new_task.id)
    session.add(link)
    session.commit()
    return task

@router.get("/", response_model=list[GlobalTaskRead])
def read_global_tasks(session: SessionDep) -> list[GlobalTaskRead]:
    global_tasks = session.exec(select(GlobalTask)).all()
    return global_tasks

@router.get("/{id}", response_model=GlobalTaskRead)
def read_global_task(id: int, session: SessionDep) -> GlobalTaskRead:
    task = session.get(GlobalTask, id)
    if not task:
        raise HTTPException(404, "GlobalTask not found")
    return task

@router.delete("/{id}")
def delete_global_task(id:int, session: SessionDep):
    global_task = session.get(GlobalTask, id)
    if not global_task:
        raise HTTPException(404, "GlobalTask not found")

    session.delete(global_task)
    session.commit()
    return {"ok": True}

@router.patch("/{id}")
def update_global_task(id:int, session:SessionDep, new_task: GlobalTaskUpdate) -> GlobalTask:
    global_task = session.get(GlobalTask, id)
    if not global_task:
        raise HTTPException(404, "GlobalTask not found")

    task_data = new_task.model_dump(exclude_unset=True)
    for key, value in task_data.items():
        setattr(global_task, key, value)

    session.add(global_task)
    session.commit()
    session.refresh(global_task)
    return global_task

@router.get("/name/{name}", response_model=list[GlobalTaskRead])
def read_global_tasks_by_name(name: str, session: SessionDep) -> list[GlobalTaskRead]:
    tasks = session.exec(
        select(GlobalTask).where(GlobalTask.name == name)
    ).all()
    if not tasks:
        raise HTTPException(404, "GlobalTasks not found")
    return tasks