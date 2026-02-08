"""
Implementation of the delete_task MCP tool.

This module implements the delete_task tool that allows users to remove tasks
through the MCP server interface.
"""
from typing import Dict, Any
from sqlmodel import Session
import logging
from ..services.task_service import delete_task as service_delete_task


# Set up logging
logger = logging.getLogger(__name__)


async def delete_task(task_id: int, db_session: Session = None, user_id: str = "default_user") -> Dict[str, Any]:
    """
    Delete a task through the MCP tool interface.

    Args:
        task_id: ID of the task to delete
        db_session: Database session for the operation
        user_id: ID of the user deleting the task

    Returns:
        Dict: Result of the operation with success status
    """
    try:
        # Validate input parameters
        if not task_id:
            return {
                "success": False,
                "message": "Task ID is required to delete a task"
            }

        # Use the task service to delete the task
        success = service_delete_task(
            session=db_session,
            task_id=str(task_id),  # Convert to string since our IDs are UUIDs
            user_id=user_id
        )

        if success:
            logger.info(f"Successfully deleted task with ID: {task_id}")
            return {
                "success": True,
                "message": "Successfully deleted the task"
            }
        else:
            logger.warning(f"Failed to delete task with ID: {task_id}")
            return {
                "success": False,
                "message": "Failed to delete the task"
            }

    except ValueError as ve:
        logger.error(f"Value error in delete_task: {ve}")
        return {
            "success": False,
            "message": f"Invalid input: {str(ve)}"
        }
    except Exception as e:
        logger.error(f"Unexpected error in delete_task: {e}")
        return {
            "success": False,
            "message": "An error occurred while deleting the task"
        }