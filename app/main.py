from typing import List

from fastapi import FastAPI

from app.api import task_api
from app.DB.db import database
from app.DB.db import Task

app = FastAPI(title="Entropy api using FastAPI, PostgresSQL and Docker")

app.include_router(task_api.router)


# DB lifecycle
@app.on_event("startup")
async def startup():
    if not database.is_connected:
        await database.connect()
# create a dummy entry
    await Task.objects.get_or_create(title="dummy title", created_by="debug_python_code")
@app.on_event("shutdown")
async def shutdown():
    if database.is_connected:
        await database.disconnect()
