from typing import Annotated
from contextlib import asynccontextmanager

from database import init_db, close_db, get_session
from sqlmodel import Session, select
from models.user import User, UserCreate, UserUpdate, UserRead

import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield
    close_db()

SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI(lifespan=lifespan)

origins = ["http://localhost:5173", "127.0.0.1:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)


@app.post("/api/users", response_model=UserCreate)
def create_user(user: UserCreate, session: SessionDep) -> User:
    new_user = User.model_validate(user)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return user

@app.get("/api/users", response_model=list[UserRead])
def read_users(session: SessionDep) -> list[UserRead]:
    users = session.exec(select(User)).all()
    return users

@app.get("/api/users/{id}", response_model=UserRead)
def read_user(id: int, session: SessionDep) -> UserRead:
    user = session.get(User, id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserRead.model_validate(user)

@app.delete("/api/users/{id}")
def delete_user(id: int, session: SessionDep):
    user = session.get(User, id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return {"ok": True}

@app.patch("/api/users/{id}")
def update_user(id: int, session: SessionDep, new_user: UserUpdate) -> User:
    user = session.get(User, id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user_data = new_user.model_dump(exclude_unset=True)
    for key, value in user_data.items():
        setattr(user, key, value)

    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@app.get("/api", summary="Main root", tags=["Main endpoints"])
async def root():
    """
    root \n
    returns json {"message":"Hello, World!"}
    """
    return {
        "message": "Hello, World!"
    }

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=8000)