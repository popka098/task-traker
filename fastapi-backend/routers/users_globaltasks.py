from fastapi import APIRouter, Depends, HTTPException

from sqlmodel import Session, select
from database import get_session

from models.user import User, UserCreate, UserUpdate, UserRead
from models.global_task import GlobalTask, GlobalTaskRead
from models.many_to_many_links.global_task_user_link import GlobalTaskUserLink

from typing import Annotated

SessionDep = Annotated[Session, Depends(get_session)]

router = APIRouter(prefix="/api/users", tags=["Users", "Users GlobalTasks", "Tasks", "GlobalTasks"])

@router.get("/{id}/resp-globaltasks", response_model=list[GlobalTaskRead])
def read_resp_global_tasks(id: int, session: SessionDep) -> list[GlobalTaskRead]:
    if not session.get(User, id):
        raise HTTPException(status_code=404, detail="User not found")

    statement = select(GlobalTask).where(GlobalTask.resp_id == id)
    res = session.exec(statement).all()
    return res

@router.post("/{id}/link-globaltask/{task_id}", response_model=GlobalTaskUserLink)
def link_user_global_task(id: int, task_id: int, session: SessionDep) -> GlobalTaskUserLink:
    user = session.get(User, id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    task = session.get(GlobalTask, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Global task not found")
    link_exists = session.exec(
        select(GlobalTaskUserLink).where(
            GlobalTaskUserLink.user_id == id,
            GlobalTaskUserLink.global_task_id == task_id
        )
    ).first()
    if link_exists:
        raise HTTPException(status_code=404, detail="Link already exists")

    link = GlobalTaskUserLink(user_id=id, global_task_id=task_id)
    session.add(link)
    session.commit()
    session.refresh(link)

    return link