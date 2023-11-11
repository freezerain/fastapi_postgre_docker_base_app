"""
This file contains utility function helpers
and playing role of mediator between FastAPI framework and PostgreSQL adapter
"""
from datetime import datetime

from typing import List

from .db import Task


async def get_all() -> List[Task]:
    return await Task.objects.all()


async def create(new_task: Task) -> Task:
    await new_task.save()
    return new_task


async def get_by_id(task_id: int) -> Task | None:
    return await Task.objects.get_or_none(id=task_id)


async def update(task_id: int, task: Task) -> Task:
    task.id = task_id
    task.updated_date = datetime.now()
    # Only this data is updated (placeholder until authentication)
    await task.update(_columns=["title", "description", "end_date", "updated_by", "updated_date"])
    # load real data from DB
    await task.load()
    return task


async def delete(task_id: int):
    task = await Task.objects.get(id=task_id)
    return await task.delete()
