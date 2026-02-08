"""
MCP tools for task operations.

This module implements the MCP tools that the AI agent will use to perform
task operations (add, list, complete, update, delete) while maintaining
statelessness and using only MCP tools for data access.
"""
from typing import Dict, Any
from sqlmodel import Session
from ..models.task import TaskCreate, TaskUpdate
from ..services import tasks as task_service


def create_add_task_tool(db_session: Session, user_id: str):
    """
    Create the add_task MCP tool function.

    Args:
        db_session: Database session for data access
        user_id: ID of the user performing the operation

    Returns:
        Function that implements the add_task operation
    """
    def add_task(title: str, description: str = None, due_date: str = None) -> Dict[str, Any]:
        """
        Create a new task.

        Args:
            title: Title of the task
            description: Optional description of the task
            due_date: Optional due date for the task

        Returns:
            Dictionary with success status and task ID
        """
        try:
            # Create task data model
            task_create = TaskCreate(
                title=title,
                description=description,
                is_completed=False  # New tasks are not completed by default
            )

            # Use the existing task service to create the task
            task = task_service.create_task(session=db_session, task=task_create, user_id=user_id)

            return {
                "success": True,
                "task_id": task.id,
                "message": f"Successfully created task '{title}'"
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error creating task: {str(e)}"
            }

    return add_task


def create_list_tasks_tool(db_session: Session, user_id: str):
    """
    Create the list_tasks MCP tool function.

    Args:
        db_session: Database session for data access
        user_id: ID of the user performing the operation

    Returns:
        Function that implements the list_tasks operation
    """
    def list_tasks(status: str = "all", limit: int = None) -> Dict[str, Any]:
        """
        List tasks based on specified criteria.

        Args:
            status: Filter tasks by status ('all', 'pending', 'completed')
            limit: Maximum number of tasks to return

        Returns:
            Dictionary with success status and list of tasks
        """
        try:
            # Get all tasks for the user
            all_tasks = task_service.get_tasks_by_user(session=db_session, user_id=user_id)

            # Filter by status if specified
            if status != "all":
                if status == "pending":
                    filtered_tasks = [task for task in all_tasks if not task.is_completed]
                elif status == "completed":
                    filtered_tasks = [task for task in all_tasks if task.is_completed]
                else:
                    filtered_tasks = all_tasks
            else:
                filtered_tasks = all_tasks

            # Apply limit if specified
            if limit is not None:
                filtered_tasks = filtered_tasks[:limit]

            # Format tasks for response
            formatted_tasks = []
            for task in filtered_tasks:
                formatted_task = {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "status": "completed" if task.is_completed else "pending",
                    "created_at": task.created_at.isoformat() if hasattr(task, 'created_at') else None
                }
                formatted_tasks.append(formatted_task)

            return {
                "success": True,
                "tasks": formatted_tasks
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error listing tasks: {str(e)}",
                "tasks": []
            }

    return list_tasks


def create_complete_task_tool(db_session: Session, user_id: str):
    """
    Create the complete_task MCP tool function.

    Args:
        db_session: Database session for data access
        user_id: ID of the user performing the operation

    Returns:
        Function that implements the complete_task operation
    """
    def complete_task(task_id: int) -> Dict[str, Any]:
        """
        Mark a task as completed.

        Args:
            task_id: ID of the task to complete

        Returns:
            Dictionary with success status and message
        """
        try:
            # Create update data
            task_update = TaskUpdate(is_completed=True)

            # Update the task
            updated_task = task_service.update_task(
                session=db_session,
                task_id=str(task_id),  # Convert to string since our IDs are UUIDs
                task_update=task_update,
                user_id=user_id
            )

            return {
                "success": True,
                "message": f"Successfully marked task '{updated_task.title}' as completed"
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error completing task: {str(e)}"
            }

    return complete_task


def create_update_task_tool(db_session: Session, user_id: str):
    """
    Create the update_task MCP tool function.

    Args:
        db_session: Database session for data access
        user_id: ID of the user performing the operation

    Returns:
        Function that implements the update_task operation
    """
    def update_task(task_id: int, title: str = None, description: str = None, due_date: str = None) -> Dict[str, Any]:
        """
        Update an existing task.

        Args:
            task_id: ID of the task to update
            title: New title for the task (optional)
            description: New description for the task (optional)
            due_date: New due date for the task (optional)

        Returns:
            Dictionary with success status and message
        """
        try:
            # Create update data
            update_data = {}
            if title is not None:
                update_data['title'] = title
            if description is not None:
                update_data['description'] = description

            task_update = TaskUpdate(**update_data)

            # Update the task
            updated_task = task_service.update_task(
                session=db_session,
                task_id=str(task_id),  # Convert to string since our IDs are UUIDs
                task_update=task_update,
                user_id=user_id
            )

            return {
                "success": True,
                "message": f"Successfully updated task"
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error updating task: {str(e)}"
            }

    return update_task


def create_delete_task_tool(db_session: Session, user_id: str):
    """
    Create the delete_task MCP tool function.

    Args:
        db_session: Database session for data access
        user_id: ID of the user performing the operation

    Returns:
        Function that implements the delete_task operation
    """
    def delete_task(task_id: int) -> Dict[str, Any]:
        """
        Delete a task.

        Args:
            task_id: ID of the task to delete

        Returns:
            Dictionary with success status and message
        """
        try:
            # Delete the task
            success = task_service.delete_task(
                session=db_session,
                task_id=str(task_id),  # Convert to string since our IDs are UUIDs
                user_id=user_id
            )

            if success:
                return {
                    "success": True,
                    "message": "Successfully deleted task"
                }
            else:
                return {
                    "success": False,
                    "message": "Failed to delete task"
                }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error deleting task: {str(e)}"
            }

    return delete_task