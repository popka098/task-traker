from typing import List

from models.base import BaseModel
from models.global_task_user_link import GlobalTaskUserLink
from sqlmodel import Field, Relationship, SQLModel

# from models.user import User


class GlobalTask(BaseModel, table=True):
    """Модель глобальной задачи

    Args:
        name (str): Название задачи.
        resp_id (int): ID ответственного за задачу пользователя.
        resp (User): ответственный за задачу пользователь.
    """
    name : str = Field(min_length=3, max_length=255, index=True)
    desc : str = Field(max_length=2048)

    resp_id : int | None = Field(default=None, foreign_key="user.id")
    resp : "User" = Relationship(back_populates="global_resp")
    workers : List["User"] = Relationship(
        back_populates="global_tasks",
        link_model=GlobalTaskUserLink
    )

class GlobalTaskCreate(SQLModel):
    name : str = Field(min_length=3, max_length=255, index=True)
    desc : str = Field(max_length=2048)
    resp_id : int | None = Field(default=None, foreign_key="user.id")

class GlobalTaskUpdate(GlobalTaskCreate):
    ...

class GlobalTaskRead(GlobalTaskCreate):
    id : int