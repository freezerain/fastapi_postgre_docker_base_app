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


async def update(task: Task):
    try:
        await task.update(description=f"this was updated from code")
    except Exception as e:
        return "error updating"
    return f"maybe was updated"


async def delete(task_id: int):
    task = await Task.objects.get(id=task_id)
    return {"deleted_rows": await task.delete()}
