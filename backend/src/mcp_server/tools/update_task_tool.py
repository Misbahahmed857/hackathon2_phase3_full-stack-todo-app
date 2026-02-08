"""
Implementation of the update_task MCP tool.

This module implements the update_task tool that allows users to update task details
through the MCP server interface.
"""
from typing import Dict, Any
from sqlmodel import Session
import logging
from ..services.task_service import update_task as service_update_task
from ..models.task import TaskUpdate


# Set up logging
logger = logging.getLogger(__name__)


async def update_task(task_id: int, title: str = None, description: str = None, due_date: str = None, db_session: Session = None, user_id: str = "default_user") -> Dict[str, Any]:
    """
    Update task details through the MCP tool interface.

    Args:
        task_id: ID of the task to update
        title: New title for the task (optional)
        description: New description for the task (optional)
        due_date: New due date for the task (optional)
        db_session: Database session for the operation
        user_id: ID of the user updating the task

    Returns:
        Dict: Result of the operation with success status and updated task details
    """
    try:
        # Validate input parameters
        if not task_id:
            return {
                "success": False,
                "message": "Task ID is required to update a task"
            }

        # Prepare update data
        update_data = {}
        if title is not None:
            update_data['title'] = title.strip()
        if description is not None:
            update_data['description'] = description.strip()
        if due_date is not None:
            update_data['due_date'] = due_date

        # Create TaskUpdate object with the provided data
        task_update = TaskUpdate(**{k: v for k, v in update_data.items() if v is not None})

        # Use the task service to update the task
        updated_task = service_update_task(
            session=db_session,
            task_id=str(task_id),  # Convert to string since our IDs are UUIDs
            task_update=task_update,
            user_id=user_id
        )

        logger.info(f"Successfully updated task with ID: {updated_task.id}")

        return {
            "success": True,
            "message": f"Successfully updated task '{updated_task.title}'",
            "task": {
                "id": updated_task.id,
                "title": updated_task.title,
                "description": updated_task.description,
                "is_completed": updated_task.is_completed,
                "updated_at": updated_task.updated_at.isoformat() if hasattr(updated_task, 'updated_at') else None
            }
        }

    except ValueError as ve:
        logger.error(f"Value error in update_task: {ve}")
        return {
            "success": False,
            "message": f"Invalid input: {str(ve)}"
        }
    except Exception as e:
        logger.error(f"Unexpected error in update_task: {e}")
        return {
            "success": False,
            "message": "An error occurred while updating the task"
        }