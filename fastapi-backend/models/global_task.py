from models.base import BaseModel
# from models.user import User

from sqlmodel import SQLModel, Field, Relationship

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

class GlobalTaskCreate(SQLModel):
    name : str = Field(min_length=3, max_length=255, index=True)
    desc : str = Field(max_length=2048)
    resp_id : int | None = Field(default=None, foreign_key="user.id")

class GlobalTaskRead(GlobalTaskCreate):
    id : int