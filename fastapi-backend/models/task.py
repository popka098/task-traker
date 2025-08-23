from sqlmodel import Field
from models.base import BaseModel


class Task(BaseModel):
    """Модель задачи

    Args:
        name (str): Название задачи.
        resp_id (int): ID ответственного за задачу пользователя.
    """
    name : str = Field(min_length=3, max_length=255, index=True)
    desc : str = Field(max_length=2048)
