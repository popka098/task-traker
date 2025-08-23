from sqlmodel import SQLModel, Field

class SubTaskUserLink(SQLModel, table=True):
    subtask_id : int | None = Field(
        default=None,
        foreign_key="subtask.id",
        primary_key=True
    )
    user_id : int | None = Field(
        default=None,
        foreign_key="user.id",
        primary_key=True
    )