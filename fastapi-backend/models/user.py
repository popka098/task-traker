from models.base import BaseModel
from sqlmodel import Field, SQLModel, Relationship
from pydantic import EmailStr
from typing import List

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
    pass

class UserRead(UserCreate):
    id : int
    is_staff : bool
    is_admin : bool

