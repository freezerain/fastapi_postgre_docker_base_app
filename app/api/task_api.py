from typing import List

from fastapi import APIRouter, HTTPException
from app.DB.db import Task
from app.DB import task_repository as repo

router = APIRouter()


# Endpoints
@router.get("/tasks", response_model=List[Task])
async def get_all_tasks():
    '''
    List all tasks
    '''
    return await repo.get_all()


@router.post("/tasks", response_model=Task, status_code=201)
async def create_task(task: Task):
    '''
    All fields are visible but not all are required
    '''
    return await repo.create(task)


@router.get("/tasks/{task_id}")
async def get_task(task_id: int):
    task = await repo.get_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/tasks/{task_id}")
async def update_task(task_id: int, task_data: Task):
    """
    Updated columns are restricted to ["title", "description", "end_date", "updated_by", "updated_date"]
    """
    task = await repo.get_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return await repo.update(task_id, task_data)


@router.delete("/tasks/{task_id}")
async def delete_task_by_id(task_id: int):
    """
    Be careful to not rm -rf
    """
    task = await repo.get_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    await repo.delete(task_id)
    return task
