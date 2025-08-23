from typing import List, TYPE_CHECKING

from models.task import Task
from models.many_to_many_links.global_task_user_link import GlobalTaskUserLink
from sqlmodel import Field, Relationship, SQLModel


class GlobalTask(Task, table=True):
    """Модель глобальной задачи

    Args:
        resp (User): ответственный за задачу пользователь.
    """
    # 1:N with User
    resp_id : int | None = Field(default=None, foreign_key="user.id")
    resp : "User" = Relationship(back_populates="global_resp")

    # N:M with User
    workers : List["User"] = Relationship(
        back_populates="global_tasks",
        link_model=GlobalTaskUserLink
    )

    # N:1 with SubTask
    subtasks: List["SubTask"] = Relationship(back_populates="global_task")

class GlobalTaskCreate(SQLModel):
    name : str = Field(min_length=3, max_length=255, index=True)
    desc : str = Field(max_length=2048)
    resp_id : int | None = Field(default=None, foreign_key="user.id")

class GlobalTaskUpdate(GlobalTaskCreate):
    ...

class GlobalTaskRead(GlobalTaskCreate):
    id : int