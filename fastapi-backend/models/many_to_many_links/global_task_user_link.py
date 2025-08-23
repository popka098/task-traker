from sqlmodel import SQLModel, Field

class GlobalTaskUserLink(SQLModel, table=True):
    global_task_id : int | None = Field(
        default=None,
        foreign_key="globaltask.id",
        primary_key=True
    )
    user_id : int | None = Field(
        default=None,
        foreign_key="user.id",
        primary_key=True
    )