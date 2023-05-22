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


class AuditMixin:
    created_by: str = ormar.String(max_length=100, default="")
    updated_by: str = ormar.String(max_length=100, default="")


class DateFieldsMixins:
    created_date: datetime.datetime = ormar.DateTime(default=datetime.datetime.now)  # pass without "()"
    updated_date: datetime.datetime = ormar.DateTime(default=datetime.datetime.now)


class Task(ormar.Model, DateFieldsMixins, AuditMixin):
    class Meta(BaseMeta):
        tablename = "tasks"

    id: int = ormar.Integer(primary_key=True)  # autoincrement = True by default
    title: str = ormar.String(max_length=128, unique=True, nullable=False)  # Required field
    description: str = ormar.String(max_length=1024, default="")
    end_date: datetime.date = ormar.DateTime(default=datetime.datetime.now() + datetime.timedelta(hours=1))


engine = sqlalchemy.create_engine(settings.db_url)
metadata.create_all(engine)