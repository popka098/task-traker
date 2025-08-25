from typing import Annotated
from contextlib import asynccontextmanager

from database import init_db, close_db, get_session
from sqlmodel import Session

import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from routers.main_router import api_router
from tags_metadata import tags_metadata


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield
    close_db()

SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI(
    lifespan=lifespan,
    openapi_tags=tags_metadata,
)

app.include_router(api_router)

origins = ["http://localhost:5173", "127.0.0.1:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

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