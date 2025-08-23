from typing import List

from sqlmodel import Field, Relationship
from models.task import Task
from models.subtask_user_link import SubTaskUserLink


class SubTask(Task, table=True):
    """Модель глобальной задачи

    Args:
        resp (User): ответственный за задачу пользователь.
    """

    workers : List["User"] = Relationship(
        back_populates="subtasks",
        link_model=SubTaskUserLink,
    )
    global_task_id : int | None = Field(default=None, foreign_key="globaltask.id")
    global_task: "GlobalTask" = Relationship(back_populates="subtasks")

