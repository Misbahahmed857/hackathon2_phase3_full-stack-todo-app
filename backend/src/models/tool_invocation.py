from sqlmodel import SQLModel, Field
from uuid import uuid4
from datetime import datetime
from typing import Optional
from sqlalchemy import Column, DateTime, JSON
import sqlalchemy.sql.functions


class ToolInvocationBase(SQLModel):
    tool_name: str = Field(max_length=100, nullable=False)
    tool_arguments: Optional[dict] = Field(default=None, sa_column=Column(JSON))
    tool_result: Optional[dict] = Field(default=None, sa_column=Column(JSON))
    status: str = Field(default="pending", max_length=50)  # pending, success, error


class ToolInvocation(ToolInvocationBase, table=True):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    user_id: str = Field(foreign_key="user.id", nullable=False)
    conversation_id: Optional[str] = Field(foreign_key="conversation.id", nullable=True)
    error_message: Optional[str] = Field(default=None, max_length=1000)
    created_at: datetime = Field(sa_column=Column(DateTime(timezone=True), default=sqlalchemy.sql.functions.now()))
    completed_at: Optional[datetime] = Field(default=None, sa_column=Column(DateTime(timezone=True)))


class ToolInvocationCreate(ToolInvocationBase):
    user_id: str
    conversation_id: Optional[str] = None


class ToolInvocationRead(ToolInvocationBase):
    id: str
    user_id: str
    conversation_id: Optional[str]
    error_message: Optional[str]
    created_at: datetime
    completed_at: Optional[datetime]
