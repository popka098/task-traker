from fastapi import APIRouter, Depends, HTTPException

from sqlmodel import Session
from database import get_session

from typing import Annotated

SessionDep = Annotated[Session, Depends(get_session)]

router = APIRouter(prefix="/api/globaltasks", tags=["GlobalTasks SubTasks"])
