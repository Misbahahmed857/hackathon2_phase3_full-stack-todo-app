"""
Task data model for the MCP server.

This module defines the Task model using SQLModel to represent tasks in the database,
following the same structure as the existing task model but within the MCP server
namespace for proper separation of concerns.
"""
from sqlmodel import SQLModel, Field
from uuid import uuid4
from datetime import datetime
from typing import Optional
from sqlalchemy import Column, DateTime
import sqlalchemy.sql.functions


class TaskBase(SQLModel):
    """Base class for task models containing common fields."""
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    is_completed: bool = Field(default=False)


class Task(TaskBase, table=True):
    """Task model representing a task in the database."""
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    user_id: str = Field(nullable=False)
    created_at: datetime = Field(sa_column=Column(DateTime(timezone=True), default=sqlalchemy.sql.functions.now()))
    updated_at: datetime = Field(sa_column=Column(DateTime(timezone=True), default=sqlalchemy.sql.functions.now(), onupdate=sqlalchemy.sql.functions.now()))


class TaskCreate(TaskBase):
    """Model for creating new tasks."""
    pass


class TaskRead(TaskBase):
    """Model for reading task data."""
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime


class TaskUpdate(SQLModel):
    """Model for updating existing tasks."""
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    is_completed: Optional[bool] = None


class TaskPatch(SQLModel):
    """Model for partially updating tasks."""
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    is_completed: Optional[bool] = None