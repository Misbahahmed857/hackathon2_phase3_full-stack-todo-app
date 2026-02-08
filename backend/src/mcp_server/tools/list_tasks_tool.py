"""
Implementation of the list_tasks MCP tool.

This module implements the list_tasks tool that allows users to retrieve their tasks
through the MCP server interface, with optional filtering capabilities.
"""
from typing import Dict, Any
from sqlmodel import Session
import logging
from ..services.task_service import get_tasks_by_user_filtered
from enum import Enum


# Set up logging
logger = logging.getLogger(__name__)


class TaskStatus(Enum):
    """Enumeration for task status filters."""
    ALL = "all"
    PENDING = "pending"
    COMPLETED = "completed"


async def list_tasks(status_filter: str = "all", limit: int = None, db_session: Session = None, user_id: str = "default_user") -> Dict[str, Any]:
    """
    Retrieve tasks for a user through the MCP tool interface.

    Args:
        status_filter: Filter tasks by status ('all', 'pending', 'completed')
        limit: Maximum number of tasks to return
        db_session: Database session for the operation
        user_id: ID of the user requesting tasks

    Returns:
        Dict: Result of the operation with success status and task list
    """
    try:
        # Validate status filter
        valid_filters = ["all", "pending", "completed"]
        if status_filter not in valid_filters:
            status_filter = "all"  # Default to all if invalid

        # Convert limit to integer if provided
        if limit is not None:
            try:
                limit = int(limit)
                if limit < 1:
                    limit = 10  # Default limit
                elif limit > 100:
                    limit = 100  # Maximum allowed limit
            except (ValueError, TypeError):
                limit = 10  # Default limit if conversion fails

        # Use the task service to get tasks with filtering
        tasks = get_tasks_by_user_filtered(
            session=db_session,
            user_id=user_id,
            status_filter=status_filter,
            limit=limit
        )

        logger.info(f"Retrieved {len(tasks)} tasks for user {user_id} with filter: {status_filter}")

        # Format tasks for response
        formatted_tasks = []
        for task in tasks:
            formatted_task = {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "status": "completed" if task.is_completed else "pending",
                "created_at": task.created_at.isoformat() if hasattr(task, 'created_at') else None,
                "updated_at": task.updated_at.isoformat() if hasattr(task, 'updated_at') else None
            }
            formatted_tasks.append(formatted_task)

        return {
            "success": True,
            "count": len(formatted_tasks),
            "status_filter": status_filter,
            "tasks": formatted_tasks,
            "message": f"Retrieved {len(formatted_tasks)} tasks"
        }

    except ValueError as ve:
        logger.error(f"Value error in list_tasks: {ve}")
        return {
            "success": False,
            "message": f"Invalid input: {str(ve)}",
            "tasks": []
        }
    except Exception as e:
        logger.error(f"Unexpected error in list_tasks: {e}")
        return {
            "success": False,
            "message": "An error occurred while retrieving tasks",
            "tasks": []
        }