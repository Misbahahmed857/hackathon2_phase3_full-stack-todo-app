"""
Conversation model for the chat system.
"""
from sqlmodel import SQLModel, Field
from uuid import uuid4
from datetime import datetime
from typing import Optional
from sqlalchemy import Column, DateTime
import sqlalchemy.sql.functions


class ConversationBase(SQLModel):
    """Base class for conversation models containing common fields."""
    user_id: str = Field(nullable=False)
    title: Optional[str] = Field(default=None, max_length=255)
    status: str = Field(default="active", max_length=50)


from sqlalchemy.schema import Index

class Conversation(ConversationBase, table=True):
    """Conversation model representing a conversation in the database."""
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    created_at: datetime = Field(sa_column=Column(DateTime(timezone=True), default=sqlalchemy.sql.functions.now()))
    updated_at: datetime = Field(sa_column=Column(DateTime(timezone=True), default=sqlalchemy.sql.functions.now(), onupdate=sqlalchemy.sql.functions.now()))

    # Indexes for performance optimization
    __table_args__ = (
        Index('idx_conversation_user_id', 'user_id'),
        Index('idx_conversation_created_at', 'created_at'),
    )


class ConversationCreate(ConversationBase):
    """Model for creating new conversations."""
    pass


class ConversationRead(ConversationBase):
    """Model for reading conversation data."""
    id: str
    created_at: datetime
    updated_at: datetime