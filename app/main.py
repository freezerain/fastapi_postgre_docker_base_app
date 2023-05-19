# app/main.py
import datetime

from fastapi import FastAPI

from app.db import database, Task

app = FastAPI(title="Entropy api using FastAPI, PostgreSQL and Docker")


# Endpoints
@app.get("/")
async def read_root():
    return await Task.objects.all()


@app.get("/tasks")
async def get_all_tasks():
    return await Task.objects.all()


@app.post("/tasks")
async def create_task():
    task = Task(title="post created title", author="create_task method")
    await task.save()  # will persist the model in database
    return f"maybe created: {task}"


@app.get("/tasks/{task_id}")
async def get_task_by_id(task_id: int):
    return await Task.objects.get(id=task_id)


@app.put("/tasks/{task_id}")
async def update_task(task_id: int):
    task = await Task.objects.get(id=task_id)

    await task.update(description=f"this was updated from code")
    return f"maybe was updated: {task}"


@app.delete("/tasks/{task_id}")
async def delete_task_by_id(task_id: int):
    task = await Task.objects.get(id=task_id)
    await task.delete()  # will delete the model from database
    return f"{task_id} maybe deleted, object: {task}"


# Lifecycle
@app.on_event("startup")
async def startup():
    if not database.is_connected:
        await database.connect()
    # create a dummy entry
    await Task.objects.get_or_create(title="dummy title", author="debug_python_code")


@app.on_event("shutdown")
async def shutdown():
    if database.is_connected:
        await database.disconnect()
