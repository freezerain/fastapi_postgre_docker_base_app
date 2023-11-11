"""
Router with all endpoints available
"""
from typing import List

from fastapi import APIRouter, HTTPException
from app.DB.db import Task
from app.DB import task_repository as repo

router = APIRouter()


@router.get("/tasks", response_model=List[Task])
async def get_all_tasks():
    """
    Get all tasks.
    :return:
    """
    return await repo.get_all()


@router.post("/tasks", response_model=Task, status_code=201)
async def create_task(task: Task):
    """
    Create task.
    Not all fields are required.
    :param task:
    :return:
    """
    return await repo.create(task)


@router.get("/tasks/{task_id}")
async def get_task(task_id: int):
    """
    Get task by ID
    :param task_id:
    :return:
    """
    task = await repo.get_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/tasks/{task_id}")
async def update_task(task_id: int, task_data: Task):
    """
    Update task by id.
    Updated columns are restricted to ["title", "description", "end_date", "updated_by", "updated_date"]
    :param task_id:
    :param task_data:
    :return:
    """
    task = await repo.get_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return await repo.update(task_id, task_data)


@router.delete("/tasks/{task_id}")
async def delete_task_by_id(task_id: int):
    """
    Remove task by id
    :param task_id:
    :return:
    """
    task = await repo.get_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    await repo.delete(task_id)
    return task
