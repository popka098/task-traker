from fastapi import APIRouter, Depends, HTTPException

from sqlmodel import Session, select
from database import get_session

from models.user import User
from models.subtask import SubTask, SubTaskRead, SubTaskCreate
from models.global_task import GlobalTask
from models.many_to_many_links.subtask_user_link import SubTaskUserLink
from models.many_to_many_links.global_task_user_link import GlobalTaskUserLink

from typing import Annotated

SessionDep = Annotated[Session, Depends(get_session)]

router = APIRouter(prefix="/api/users", tags=["Users Subtasks"])

@router.get("/{id}/subtasks", response_model=list[SubTaskRead])
def read_global_tasks_by_user(id: int, session: SessionDep) -> list[SubTaskRead]:
    user = session.get(User, id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user.subtasks

@router.post("/{id}/subtasks/{task_id}", response_model=SubTaskUserLink)
def link_user_subtask(id: int, task_id: int, session: SessionDep) -> SubTaskUserLink:
    subtask = session.get(SubTask, task_id)
    if not subtask:
        raise HTTPException(status_code=404, detail="SubTask not found")
    # user = session.get(User, id)
    user = session.exec(
        select(User.id)
        .join(GlobalTaskUserLink, User.id == GlobalTaskUserLink.user_id)
        .join(GlobalTask, GlobalTask.id == GlobalTaskUserLink.global_task_id)
        .join(SubTask, SubTask.global_task_id == GlobalTask.id)
        .where(
            User.id == id,
            SubTask.id == task_id
        )
    ).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    link_exists = session.exec(
        select(SubTaskUserLink).where(
            SubTaskUserLink.user_id == id,
            SubTaskUserLink.subtask_id == task_id
        )
    ).first()
    if link_exists:
        raise HTTPException(status_code=404, detail="Link already exists")

    link = SubTaskUserLink(user_id=id, subtask_id=task_id)
    session.add(link)
    session.commit()
    session.refresh(link)
    return link