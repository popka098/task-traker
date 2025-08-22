from models.base import BaseModel
from sqlmodel import Field, SQLModel

class User(BaseModel, table=True):
    name : str = Field(min_length=3, max_length=255, index=True)
    username : str = Field(min_length=3, max_length=255, unique=True)

class UserCreate(SQLModel):
    name : str = Field(min_length=3, max_length=255, index=True)
    username : str = Field(min_length=3, max_length=255, unique=True)

class UserUpdate(SQLModel):
    name : str = Field(min_length=3, max_length=255, index=True)
    username : str = Field(min_length=3, max_length=255, unique=True)

class UserRead(SQLModel):
    id : int
    name : str
    username : str

