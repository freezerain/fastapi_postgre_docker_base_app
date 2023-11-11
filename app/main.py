import datetime
from typing import List

from fastapi import FastAPI

from app.api import task_api
from app.DB.db import database
from app.DB.db import Task

# This is a FastApi api app dockerized and connected to PostgresSql docker image
# multiple sanity tests are present as well as data model for presentation
# basic data validation
# @url http://127.0.0.1:8008/
# @author Ilia Rodikov
# @email freeze.eli@google.com

app = FastAPI(title="Api using FastAPI, PostgresSQL and Docker",
              description="This project template serves as a versatile starting point for various future projects.",
              version="0.2.1",
              contact={
                  "name": "Ilia Rodikov",
                  "url": "https://www.linkedin.com/in/elrodikov/",
                  "email": "freeze.eli@google.com",
              },
              docs_url="/", )


# App-db lifecycle
@app.on_event("startup")
async def startup():
    if not database.is_connected:
        await database.connect()
    # create a dummy entries
    try:
        await __mock_data()
    except Exception as e:
        # This needed only if title already exists with another ID - limitation of current data model
        pass


@app.on_event("shutdown")
async def shutdown():
    if database.is_connected:
        await database.disconnect()


app.include_router(task_api.router)


async def __mock_data():
    await Task.objects.get_or_create(title="Robot war 2", created_by="main.py",
                                     description="$$$Its time to get some money$$$")
    await Task.objects.get_or_create(title="pillow fight this night", created_by="main.py")
    await Task.objects.get_or_create(title="TEDx: how to be more happy eating brown rice", created_by="papa",
                                     end_date=datetime.datetime.now() + datetime.timedelta(days=1054))
