from fastapi import APIRouter
from routers import users, global_tasks, users_globaltasks, users_subtasks, globaltasks_subtasks, subtasks

api_router = APIRouter()

api_router.include_router(users.router)
api_router.include_router(global_tasks.router)
api_router.include_router(users_globaltasks.router)
api_router.include_router(users_subtasks.router)
api_router.include_router(globaltasks_subtasks.router)
api_router.include_router(subtasks.router)