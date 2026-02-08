"""
Implementation of the add_task MCP tool.

This module implements the add_task tool that allows users to create new tasks
through the MCP server interface, following the constitutional requirements
for stateless operation and MCP-only database access.
"""
from typing import Dict, Any
from sqlmodel import Session
import logging
from ..services.task_service import create_task
from ..models.task import TaskCreate


# Set up logging
logger = logging.getLogger(__name__)


async def add_task(title: str, description: str = None, due_date: str = None, db_session: Session = None, user_id: str = "default_user") -> Dict[str, Any]:
    """
    Create a new task through the MCP tool interface.

    Args:
        title: Title of the task to create
        description: Optional description of the task
        due_date: Optional due date for the task
        db_session: Database session for the operation
        user_id: ID of the user creating the task

    Returns:
        Dict: Result of the operation with success status and task details
    """
    try:
        # Validate input parameters
        if not title or not title.strip():
            return {
                "success": False,
                "message": "Title is required for creating a task"
            }

        # Create task data model
        task_create = TaskCreate(
            title=title.strip(),
            description=description.strip() if description else None,
            is_completed=False  # New tasks are not completed by default
        )

        # Use the task service to create the task
        created_task = create_task(
            session=db_session,
            task=task_create,
            user_id=user_id
        )

        logger.info(f"Successfully created task with ID: {created_task.id}")

        return {
            "success": True,
            "task_id": created_task.id,
            "message": f"Successfully created task '{title}'",
            "task": {
                "id": created_task.id,
                "title": created_task.title,
                "description": created_task.description,
                "is_completed": created_task.is_completed,
                "created_at": created_task.created_at.isoformat() if hasattr(created_task, 'created_at') else None
            }
        }

    except ValueError as ve:
        logger.error(f"Value error in add_task: {ve}")
        return {
            "success": False,
            "message": f"Invalid input: {str(ve)}"
        }
    except Exception as e:
        logger.error(f"Unexpected error in add_task: {e}")
        return {
            "success": False,
            "message": "An error occurred while creating the task"
        }