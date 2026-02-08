"""
Chat API router for handling chat conversations and messages.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Optional
from sqlmodel import Session
import json

from src.api.deps import get_current_user
from src.database import get_session
from src.models.user import User
from src.services.chat_service import create_conversation, get_conversation_by_id, create_message, get_messages_by_conversation
from src.models.conversation import ConversationCreate
from src.models.message import MessageCreate

router = APIRouter(prefix="/chat", tags=["chat"])

# Import models from the dedicated models file
from .models import ChatMessage, ChatRequest, ChatResponse, ErrorResponse


@router.post("/{user_id}/chat", response_model=ChatResponse)
async def chat_endpoint(
    user_id: str,
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """
    Chat endpoint that handles user messages and returns AI responses.

    Args:
        user_id: ID of the user sending the message
        request: Chat request containing message and optional conversation_id
        current_user: The authenticated user making the request
        db: Database session for operations

    Returns:
        ChatResponse: Response containing AI message and conversation info
    """
    try:
        # Verify that the user_id matches the authenticated user
        if current_user.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authorized to access this conversation"
            )

        # Get or create conversation
        conversation = None
        if request.conversation_id:
            conversation = get_conversation_by_id(
                db_session=db,
                conversation_id=request.conversation_id,
                user_id=user_id
            )
            if not conversation:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Conversation not found"
                )
        else:
            # Create a new conversation
            conversation = create_conversation(
                db_session=db,
                user_id=user_id,
                title=f"Chat started on {current_user.email or user_id}"
            )

        # Save user message to the conversation
        user_message = create_message(
            db_session=db,
            message_create=MessageCreate(
                conversation_id=conversation.id,
                role=request.message.role,
                content=request.message.content,
                message_type="text"
            ),
            conversation_id=conversation.id,
            role=request.message.role,
            content=request.message.content
        )

        # Process the user message with the AI agent
        from src.services.chat_service import process_message_with_ai_agent

        # Get API key from environment
        import os
        api_key = os.getenv("OPENROUTER_API_KEY")

        ai_response = process_message_with_ai_agent(
            db_session=db,
            conversation_id=conversation.id,
            user_id=user_id,
            user_message_content=request.message.content,
            api_key=api_key
        )

        ai_response_content = ai_response["content"]
        tool_calls = ai_response.get("tool_calls", [])

        # Save AI response to the conversation
        ai_message = create_message(
            db_session=db,
            message_create=MessageCreate(
                conversation_id=conversation.id,
                role="assistant",
                content=ai_response_content,
                message_type="text"
            ),
            conversation_id=conversation.id,
            role="assistant",
            content=ai_response_content
        )

        # Prepare response
        response = ChatResponse(
            success=True,
            message={
                "id": str(ai_message.id),
                "content": ai_message.content,
                "role": ai_message.role,
                "timestamp": ai_message.timestamp.isoformat(),
                "type": ai_message.message_type
            },
            conversation_id=conversation.id,
            tool_calls=tool_calls
        )

        return response

    except HTTPException:
        # Re-raise HTTP exceptions (like 401, 404) as they are
        raise
    except Exception as e:
        # Log the error for debugging
        import logging
        logging.error(f"Error in chat endpoint: {str(e)}")

        # Return a user-friendly error response
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while processing your request"
        )