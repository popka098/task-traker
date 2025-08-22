from sqlmodel import SQLModel, Field

class BaseModel(SQLModel):
    id : int | None = Field(default=None, primary_key=True, unique=True)