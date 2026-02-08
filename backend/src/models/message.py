"""
Message model for the chat system.
"""
from sqlmodel import SQLModel, Field
from uuid import uuid4
from datetime import datetime
from typing import Optional
from sqlalchemy import Column, DateTime
import sqlalchemy.sql.functions
import json


class MessageBase(SQLModel):
    """Base class for message models containing common fields."""
    conversation_id: str = Field(nullable=False)  # Foreign key reference to conversation
    role: str = Field(max_length=20)  # user, assistant, system
    content: str = Field()
    message_type: str = Field(default="text", max_length=50)  # text, tool_call, tool_response


from sqlalchemy.schema import Index

class Message(MessageBase, table=True):
    """Message model representing a message in the database."""
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    timestamp: datetime = Field(sa_column=Column(DateTime(timezone=True), default=sqlalchemy.sql.functions.now()))
    metadata_json: Optional[str] = Field(default=None)  # JSON string for additional metadata

    # Indexes for performance optimization
    __table_args__ = (
        Index('idx_message_conversation_timestamp', 'conversation_id', 'timestamp'),
        Index('idx_message_role', 'role'),
    )


class MessageCreate(MessageBase):
    """Model for creating new messages."""
    pass


class MessageRead(MessageBase):
    """Model for reading message data."""
    id: str
    timestamp: datetime
    metadata_dict: Optional[dict] = None  # Helper to convert metadata_json to dict

    def __init__(self, **data):
        super().__init__(**data)
        if self.metadata_json:
            try:
                self.metadata_dict = json.loads(self.metadata_json)
            except (json.JSONDecodeError, TypeError):
                self.metadata_dict = {}