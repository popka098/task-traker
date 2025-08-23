from models.base import BaseModel
from sqlmodel import Field, SQLModel
from pydantic import EmailStr

class User(BaseModel, table=True):
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
    email : EmailStr
    is_stuff : bool = Field(default=False)
    is_admin : bool = Field(default=False)

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
    email : EmailStr

class UserUpdate(UserCreate):
    pass

class UserRead(UserCreate):
    id : int
    is_stuff : bool
    is_admin : bool

