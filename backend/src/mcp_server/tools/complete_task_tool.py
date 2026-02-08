"""
Implementation of the complete_task MCP tool.

This module implements the complete_task tool that allows users to mark tasks as completed
through the MCP server interface.
"""
from typing import Dict, Any
from sqlmodel import Session
import logging
from ..services.task_service import complete_task as service_complete_task
from ..models.task import TaskUpdate


# Set up logging
logger = logging.getLogger(__name__)


async def complete_task(task_id: int, db_session: Session = None, user_id: str = "default_user") -> Dict[str, Any]:
    """
    Mark a task as completed through the MCP tool interface.

    Args:
        task_id: ID of the task to mark as completed
        db_session: Database session for the operation
        user_id: ID of the user marking the task as completed

    Returns:
        Dict: Result of the operation with success status and task details
    """
    try:
        # Validate input parameters
        if not task_id:
            return {
                "success": False,
                "message": "Task ID is required to complete a task"
            }

        # Use the task service to complete the task
        updated_task = service_complete_task(
            session=db_session,
            task_id=str(task_id),  # Convert to string since our IDs are UUIDs
            user_id=user_id
        )

        logger.info(f"Successfully completed task with ID: {updated_task.id}")

        return {
            "success": True,
            "message": f"Successfully marked task '{updated_task.title}' as completed",
            "task": {
                "id": updated_task.id,
                "title": updated_task.title,
                "description": updated_task.description,
                "is_completed": updated_task.is_completed,
                "updated_at": updated_task.updated_at.isoformat() if hasattr(updated_task, 'updated_at') else None
            }
        }

    except ValueError as ve:
        logger.error(f"Value error in complete_task: {ve}")
        return {
            "success": False,
            "message": f"Invalid input: {str(ve)}"
        }
    except Exception as e:
        logger.error(f"Unexpected error in complete_task: {e}")
        return {
            "success": False,
            "message": "An error occurred while completing the task"
        }