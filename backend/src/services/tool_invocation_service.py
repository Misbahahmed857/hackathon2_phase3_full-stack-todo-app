"""
Service for logging and tracking tool invocations.
"""
import logging
from sqlmodel import Session
from typing import Optional, Dict, Any
from datetime import datetime

from src.models.tool_invocation import ToolInvocation, ToolInvocationCreate, ToolInvocationRead

# Set up logging
logger = logging.getLogger(__name__)


def create_tool_invocation(
    *,
    db_session: Session,
    user_id: str,
    conversation_id: Optional[str],
    tool_name: str,
    tool_arguments: Optional[Dict[str, Any]] = None
) -> ToolInvocation:
    """
    Create a new tool invocation record.

    Args:
        db_session: Database session for the operation
        user_id: ID of the user who triggered the tool
        conversation_id: ID of the conversation (if applicable)
        tool_name: Name of the tool being invoked
        tool_arguments: Arguments passed to the tool

    Returns:
        ToolInvocation: The created tool invocation record
    """
    logger.info(f"Creating tool invocation record: {tool_name} for user {user_id}")

    tool_invocation = ToolInvocation(
        user_id=user_id,
        conversation_id=conversation_id,
        tool_name=tool_name,
        tool_arguments=tool_arguments,
        status="pending"
    )

    db_session.add(tool_invocation)
    db_session.commit()
    db_session.refresh(tool_invocation)

    logger.info(f"Successfully created tool invocation {tool_invocation.id}")

    return tool_invocation


def update_tool_invocation_result(
    *,
    db_session: Session,
    tool_invocation_id: str,
    status: str,
    tool_result: Optional[Dict[str, Any]] = None,
    error_message: Optional[str] = None
) -> ToolInvocation:
    """
    Update a tool invocation with its result.

    Args:
        db_session: Database session for the operation
        tool_invocation_id: ID of the tool invocation to update
        status: Status of the invocation (success or error)
        tool_result: Result data from the tool execution
        error_message: Error message if the invocation failed

    Returns:
        ToolInvocation: The updated tool invocation record
    """
    logger.info(f"Updating tool invocation {tool_invocation_id} with status {status}")

    tool_invocation = db_session.get(ToolInvocation, tool_invocation_id)

    if not tool_invocation:
        logger.error(f"Tool invocation {tool_invocation_id} not found")
        raise ValueError(f"Tool invocation {tool_invocation_id} not found")

    tool_invocation.status = status
    tool_invocation.tool_result = tool_result
    tool_invocation.error_message = error_message
    tool_invocation.completed_at = datetime.now()

    db_session.add(tool_invocation)
    db_session.commit()
    db_session.refresh(tool_invocation)

    logger.info(f"Successfully updated tool invocation {tool_invocation_id}")

    return tool_invocation
