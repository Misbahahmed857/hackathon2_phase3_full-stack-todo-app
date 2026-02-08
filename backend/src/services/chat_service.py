"""
Chat service for handling conversation and message operations.
"""
import logging
from sqlmodel import Session, select
from typing import List, Optional
from datetime import datetime
from uuid import uuid4

from src.models.conversation import Conversation, ConversationCreate, ConversationRead
from src.models.message import Message, MessageCreate, MessageRead

# Set up logging
logger = logging.getLogger(__name__)


def create_conversation(*, db_session: Session, user_id: str, title: Optional[str] = None) -> ConversationRead:
    """
    Create a new conversation for a user.

    Args:
        db_session: Database session for the operation
        user_id: ID of the user creating the conversation
        title: Optional title for the conversation

    Returns:
        ConversationRead: The created conversation
    """
    logger.info(f"Creating new conversation for user {user_id}")

    conversation = Conversation(
        user_id=user_id,
        title=title or f"Conversation {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        status="active"
    )

    db_session.add(conversation)
    db_session.commit()
    db_session.refresh(conversation)

    logger.info(f"Successfully created conversation {conversation.id} for user {user_id}")

    return ConversationRead.model_validate(conversation.model_dump())


def get_conversation_by_id(*, db_session: Session, conversation_id: str, user_id: str) -> Optional[ConversationRead]:
    """
    Get a conversation by ID for a specific user.

    Args:
        db_session: Database session for the operation
        conversation_id: ID of the conversation to retrieve
        user_id: ID of the user requesting the conversation

    Returns:
        ConversationRead: The conversation if found and belongs to user, None otherwise
    """
    logger.debug(f"Retrieving conversation {conversation_id} for user {user_id}")

    statement = select(Conversation).where(
        Conversation.id == conversation_id,
        Conversation.user_id == user_id
    )
    conversation = db_session.exec(statement).first()

    if conversation:
        logger.debug(f"Found conversation {conversation_id} for user {user_id}")
        return ConversationRead.model_validate(conversation.model_dump())
    else:
        logger.debug(f"Conversation {conversation_id} not found for user {user_id}")
        return None


def create_message(*, db_session: Session, message_create: MessageCreate, conversation_id: str, role: str, content: str) -> MessageRead:
    """
    Create a new message in a conversation.

    Args:
        db_session: Database session for the operation
        message_create: Message creation data
        conversation_id: ID of the conversation to add message to
        role: Role of the message sender (user, assistant, system)
        content: Content of the message

    Returns:
        MessageRead: The created message
    """
    logger.info(f"Creating new message in conversation {conversation_id}, role: {role}")

    message = Message(
        conversation_id=conversation_id,
        role=role,
        content=content,
        message_type=message_create.message_type
    )

    db_session.add(message)
    db_session.commit()
    db_session.refresh(message)

    logger.info(f"Successfully created message {message.id} in conversation {conversation_id}")

    return MessageRead.model_validate(message.model_dump())


def get_messages_by_conversation(*, db_session: Session, conversation_id: str, user_id: str) -> List[MessageRead]:
    """
    Get all messages for a conversation, ensuring user has access to the conversation.

    Args:
        db_session: Database session for the operation
        conversation_id: ID of the conversation to retrieve messages from
        user_id: ID of the user requesting the messages

    Returns:
        List[MessageRead]: List of messages in the conversation
    """
    logger.debug(f"Retrieving messages for conversation {conversation_id} for user {user_id}")

    # First verify the user has access to this conversation
    conv_statement = select(Conversation).where(
        Conversation.id == conversation_id,
        Conversation.user_id == user_id
    )
    conversation = db_session.exec(conv_statement).first()

    if not conversation:
        logger.warning(f"User {user_id} does not have access to conversation {conversation_id}")
        return []  # User doesn't have access to this conversation

    # Get messages for the conversation
    msg_statement = select(Message).where(
        Message.conversation_id == conversation_id
    ).order_by(Message.timestamp.asc())

    messages = db_session.exec(msg_statement).all()

    logger.debug(f"Retrieved {len(messages)} messages for conversation {conversation_id}")

    return [MessageRead.model_validate(msg.model_dump()) for msg in messages]


def update_conversation_title(*, db_session: Session, conversation_id: str, user_id: str, new_title: str) -> Optional[ConversationRead]:
    """
    Update the title of a conversation.

    Args:
        db_session: Database session for the operation
        conversation_id: ID of the conversation to update
        user_id: ID of the user requesting the update
        new_title: New title for the conversation

    Returns:
        ConversationRead: Updated conversation if successful, None otherwise
    """
    logger.info(f"Updating title for conversation {conversation_id} for user {user_id}")

    statement = select(Conversation).where(
        Conversation.id == conversation_id,
        Conversation.user_id == user_id
    )
    conversation = db_session.exec(statement).first()

    if not conversation:
        logger.warning(f"User {user_id} does not have access to conversation {conversation_id} or it doesn't exist")
        return None

    conversation.title = new_title
    conversation.updated_at = datetime.now()

    db_session.add(conversation)
    db_session.commit()
    db_session.refresh(conversation)

    logger.info(f"Successfully updated title for conversation {conversation_id}")

    return ConversationRead.model_validate(conversation.model_dump())


def process_message_with_ai_agent(*, db_session: Session, conversation_id: str, user_id: str, user_message_content: str, api_key: Optional[str] = None) -> dict:
    """
    Process a user message with the AI agent and return the AI response.

    Args:
        db_session: Database session for the operation
        conversation_id: ID of the conversation
        user_id: ID of the user
        user_message_content: Content of the user message
        api_key: OpenRouter API key (if not provided, will use environment variable)

    Returns:
        dict: AI response content and any tool calls made
    """
    logger.info(f"Processing message for user {user_id} in conversation {conversation_id}")

    from src.agents.ai_agent import AIAgent
    import os

    # Get conversation history for context
    logger.debug(f"Fetching conversation history for conversation {conversation_id}")
    conversation_history = get_messages_by_conversation(
        db_session=db_session,
        conversation_id=conversation_id,
        user_id=user_id
    )

    # Format the conversation history for the AI agent
    formatted_history = []
    for msg in conversation_history:
        formatted_history.append({
            "role": msg.role,
            "content": msg.content
        })

    logger.debug(f"Formatted {len(formatted_history)} messages for AI processing")

    # Get API key from parameter or environment
    effective_api_key = api_key or os.getenv("OPENROUTER_API_KEY")
    if not effective_api_key:
        logger.warning("OpenRouter API key not configured, returning placeholder response")
        # For development/testing purposes, return a placeholder response
        return {
            "content": f"AI Agent: I received your message: '{user_message_content}'. [Note: OpenRouter API key not configured]",
            "tool_calls": []
        }

    try:
        logger.debug("Initializing AI agent")
        agent = AIAgent(api_key=effective_api_key)

        # Process the user message with the AI agent
        logger.info(f"Sending message to AI agent: '{user_message_content[:50]}...'")
        ai_response_content = agent.process_request(
            user_input=user_message_content,
            user_id=user_id,
            db_session=db_session,
            conversation_history=formatted_history,
            conversation_id=conversation_id
        )

        logger.info(f"Received response from AI agent for conversation {conversation_id}")

        return {
            "content": ai_response_content,
            "tool_calls": []  # In the current implementation, tool calls are handled internally by the agent
        }
    except Exception as e:
        # Log the error and return a user-friendly message
        logger.error(f"Error processing AI request for user {user_id} in conversation {conversation_id}: {str(e)}")
        return {
            "content": f"I'm sorry, I encountered an error processing your request: {str(e)}",
            "tool_calls": []
        }