"""
Request and response models for the chat API.
"""
from pydantic import BaseModel, validator, Field
from typing import Optional, List
from datetime import datetime
import html


class ChatMessage(BaseModel):
    """Model for chat message in request."""
    content: str = Field(..., min_length=1, max_length=10000)  # Limit content length
    role: str = Field(default="user", pattern="^(user|assistant|system)$")  # Restrict role values

    @validator('content')
    def sanitize_content(cls, v):
        """Sanitize content to prevent XSS and other injection attacks."""
        # Strip leading/trailing whitespace
        v = v.strip()

        # Sanitize HTML content to prevent XSS
        # This is a basic sanitization - in production, consider using a proper HTML sanitizer
        v = html.escape(v)

        # Additional sanitization could be added here
        return v


class ChatRequest(BaseModel):
    """Model for chat request."""
    message: ChatMessage
    conversation_id: Optional[str] = Field(None, min_length=1, max_length=100)  # Validate conversation_id if provided


class ChatResponse(BaseModel):
    """Model for chat response."""
    success: bool
    message: dict
    conversation_id: str
    tool_calls: Optional[List[dict]] = []


class ErrorResponse(BaseModel):
    """Model for error responses."""
    error: str
    code: str
    details: Optional[dict] = None