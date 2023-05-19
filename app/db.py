# app/db.py
import datetime

import databases
import ormar
import sqlalchemy

from .config import settings

database = databases.Database(settings.db_url)
metadata = sqlalchemy.MetaData()


class BaseMeta(ormar.ModelMeta):
    metadata = metadata
    database = database


class Task(ormar.Model):
    class Meta(BaseMeta):
        tablename = "tasks"

    id: int = ormar.Integer(primary_key=True)
    title: str = ormar.String(max_length=128, unique=True, nullable=False)
    description: str = ormar.String(max_length=1024, default=None, nullable=True)
    creating_date: datetime.date = ormar.Date(default=datetime.datetime.now(), nullable=False)
    end_date: datetime.date = ormar.Date(default=datetime.datetime.now(), nullable=False)
    # placeholder until user table exists
    author: str = ormar.String(max_length=128, nullable=False)


engine = sqlalchemy.create_engine(settings.db_url)
metadata.create_all(engine)
