# app/main.py

from fastapi import FastAPI

from app.db import database, Task


app = FastAPI(title="Entropy api using FastAPI, PostgreSQL and Docker")


@app.get("/")
async def read_root():
    return await Task.objects.all()


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