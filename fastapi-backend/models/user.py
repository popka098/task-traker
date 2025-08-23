from typing import List

from models.base import BaseModel
from models.global_task_user_link import GlobalTaskUserLink
from models.subtask_user_link import SubTaskUserLink
from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel


class User(BaseModel, table=True):
    """Модель пользователя

    Args:
        name (str): Имя пользователя
        username (str): Уникальное имя пользователя
        email (EmailStr): Электронная почта пользователя
        is_staff (bool): Является ли персоналом
        is_admin (bool): Является ли админом
        global_resp (List["GlobalTask"]): Глобальные задачи, за которые ответственен
    """
    name : str = Field(
        min_length=3,
        max_length=255,
        index=True
    )
    username : str = Field(
        min_length=3,
        max_length=255,
        unique=True
    )
    email : EmailStr = Field(unique=True)
    is_staff : bool = Field(default=False)
    is_admin : bool = Field(default=False)

    global_resp : List["GlobalTask"] = Relationship(back_populates="resp")
    global_tasks: List["GlobalTask"] = Relationship(
        back_populates="workers",
        link_model=GlobalTaskUserLink
    )
    subtasks: List["SubTask"] = Relationship(
        back_populates="workers",
        link_model=SubTaskUserLink
    )

class UserCreate(SQLModel):
    name : str = Field(
        min_length=3,
        max_length=255,
        index=True
    )
    username : str = Field(
        min_length=3,
        max_length=255,
        unique=True
    )
    email : EmailStr = Field(unique=True)

class UserUpdate(UserCreate):
    ...

class UserRead(UserCreate):
    id : int
    is_staff : bool
    is_admin : bool

