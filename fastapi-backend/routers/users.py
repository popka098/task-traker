from fastapi import APIRouter, Depends, HTTPException

from sqlmodel import Session, select
from database import get_session

from models.user import User, UserCreate, UserUpdate, UserRead

from typing import Annotated

SessionDep = Annotated[Session, Depends(get_session)]

router = APIRouter(prefix="/api/users", tags=["Users"])

@router.post("/", response_model=UserCreate)
def create_user(user: UserCreate, session: SessionDep) -> User:
    new_user = User.model_validate(user)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return user

@router.get("/", response_model=list[UserRead])
def read_users(session: SessionDep) -> list[UserRead]:
    users = session.exec(select(User)).all()
    return users

@router.get("/{id}", response_model=UserRead)
def read_user(id: int, session: SessionDep) -> UserRead:
    user = session.get(User, id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserRead.model_validate(user)

@router.delete("/{id}")
def delete_user(id: int, session: SessionDep):
    user = session.get(User, id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return {"ok": True}

@router.patch("/{id}")
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

@router.get("/username/{username}", response_model=UserRead)
def read_user_by_username(username: str, session: SessionDep) -> UserRead:
    user = session.exec(
        select(User).where(username == User.username)
    ).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user
