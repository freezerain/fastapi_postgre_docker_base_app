from datetime import datetime
from typing import List

from .db import Task


async def get_all() -> List[Task]:
    return await Task.objects.all()


async def create(new_task: Task) -> Task:
    await new_task.save()
    # try:
    #     await task.save()
    # except ValidationError as e:
    #     raise HTTPException(status_code=422, detail=f"Data not valid\n{str(e)}")
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=f"---SAVING ERROR---\n{str(e)}")
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
