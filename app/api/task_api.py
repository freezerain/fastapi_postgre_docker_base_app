from typing import List

from fastapi import APIRouter
from app.DB.db import Task
from app.DB import task_repository as repo

router = APIRouter()


@router.get("/")
async def get_root():
    return {"msg": "Hello World!"}


@router.get("/tasks", response_model=List[Task])
async def get_all_tasks():
    return await repo.get_all()


@router.post("/tasks", response_model=Task, status_code=201)
async def create_task(task: Task):
    return await repo.create(task)


@router.get("/tasks/{task_id}")
async def get_task(task_id: int):
    return await repo.get_by_id(task_id)


@router.put("/tasks/{task_id}")
async def update_task(task: Task):
    return await repo.update(task)


@router.delete("/tasks/{task_id}")
async def delete_task_by_id(task_id: int):
    return await repo.delete(task_id)
