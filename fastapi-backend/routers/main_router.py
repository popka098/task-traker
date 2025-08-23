from fastapi import APIRouter
from routers import users, global_tasks

api_router = APIRouter()

api_router.include_router(users.router)
api_router.include_router(global_tasks.router)