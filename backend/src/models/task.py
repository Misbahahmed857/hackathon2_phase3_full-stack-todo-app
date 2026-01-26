from sqlmodel import SQLModel, Field
from uuid import uuid4
from datetime import datetime
from typing import Optional
from sqlalchemy import Column, DateTime
import sqlalchemy.sql.functions


class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    is_completed: bool = Field(default=False)


class Task(TaskBase, table=True):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    user_id: str = Field(foreign_key="user.id", nullable=False)
    created_at: datetime = Field(sa_column=Column(DateTime(timezone=True), default=sqlalchemy.sql.functions.now()))
    updated_at: datetime = Field(sa_column=Column(DateTime(timezone=True), default=sqlalchemy.sql.functions.now(), onupdate=sqlalchemy.sql.functions.now()))


class TaskCreate(TaskBase):
    pass


class TaskRead(TaskBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime


class TaskUpdate(SQLModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    is_completed: Optional[bool] = None


class TaskPatch(SQLModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    is_completed: Optional[bool] = None