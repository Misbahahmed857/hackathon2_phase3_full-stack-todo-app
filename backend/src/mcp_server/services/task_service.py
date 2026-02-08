"""
Business logic for task operations in the MCP server.

This module implements the business logic for task operations (create, read, update, delete)
following the same patterns as the existing task service but adapted for the MCP server
architecture and stateless operation requirements.
"""
from sqlmodel import Session, select
from typing import List, Optional
from ..models.task import Task, TaskCreate, TaskUpdate, TaskRead, TaskPatch
from fastapi import HTTPException, status


def create_task(*, session: Session, task: TaskCreate, user_id: str) -> TaskRead:
    """
    Create a new task for the authenticated user.

    Args:
        session: Database session for the operation
        task: Task creation data
        user_id: ID of the user creating the task

    Returns:
        TaskRead: Created task data
    """
    db_task = Task(
        title=task.title,
        description=task.description,
        is_completed=task.is_completed,
        user_id=user_id
    )

    session.add(db_task)
    session.commit()
    session.refresh(db_task)

    return TaskRead.model_validate(db_task.model_dump())


def get_tasks_by_user(*, session: Session, user_id: str) -> List[TaskRead]:
    """
    Get all tasks for the authenticated user.

    Args:
        session: Database session for the operation
        user_id: ID of the user whose tasks to retrieve

    Returns:
        List[TaskRead]: List of user's tasks
    """
    statement = select(Task).where(Task.user_id == user_id)
    tasks = session.exec(statement).all()

    return [TaskRead.model_validate(task.model_dump()) for task in tasks]


def get_tasks_by_user_filtered(*, session: Session, user_id: str, status_filter: Optional[str] = None, limit: Optional[int] = None) -> List[TaskRead]:
    """
    Get tasks for the user with optional filtering.

    Args:
        session: Database session for the operation
        user_id: ID of the user whose tasks to retrieve
        status_filter: Filter by status ('all', 'pending', 'completed')
        limit: Maximum number of tasks to return

    Returns:
        List[TaskRead]: List of filtered tasks
    """
    statement = select(Task).where(Task.user_id == user_id)

    # Apply status filter if specified
    if status_filter and status_filter != 'all':
        if status_filter == 'pending':
            statement = statement.where(Task.is_completed == False)
        elif status_filter == 'completed':
            statement = statement.where(Task.is_completed == True)

    # Execute query
    tasks = session.exec(statement).all()

    # Apply limit if specified
    if limit is not None:
        tasks = tasks[:limit]

    return [TaskRead.model_validate(task.model_dump()) for task in tasks]


def get_task_by_id(*, session: Session, task_id: str, user_id: str) -> TaskRead:
    """
    Get a specific task by ID for the authenticated user.

    Args:
        session: Database session for the operation
        task_id: ID of the task to retrieve
        user_id: ID of the user requesting the task

    Returns:
        TaskRead: The requested task data

    Raises:
        HTTPException: If task is not found
    """
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    db_task = session.exec(statement).first()

    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return TaskRead.model_validate(db_task.model_dump())


def update_task(*, session: Session, task_id: str, task_update: TaskUpdate, user_id: str) -> TaskRead:
    """
    Update a specific task for the authenticated user.

    Args:
        session: Database session for the operation
        task_id: ID of the task to update
        task_update: Task update data
        user_id: ID of the user updating the task

    Returns:
        TaskRead: Updated task data

    Raises:
        HTTPException: If task is not found
    """
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    db_task = session.exec(statement).first()

    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Update only the fields that are provided
    update_data = task_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_task, field, value)

    session.add(db_task)
    session.commit()
    session.refresh(db_task)

    return TaskRead.model_validate(db_task.model_dump())


def delete_task(*, session: Session, task_id: str, user_id: str) -> bool:
    """
    Delete a specific task for the authenticated user.

    Args:
        session: Database session for the operation
        task_id: ID of the task to delete
        user_id: ID of the user deleting the task

    Returns:
        bool: True if deletion was successful

    Raises:
        HTTPException: If task is not found
    """
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    db_task = session.exec(statement).first()

    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    session.delete(db_task)
    session.commit()

    return True


def complete_task(*, session: Session, task_id: str, user_id: str) -> TaskRead:
    """
    Mark a specific task as completed for the authenticated user.

    Args:
        session: Database session for the operation
        task_id: ID of the task to complete
        user_id: ID of the user completing the task

    Returns:
        TaskRead: Updated task data

    Raises:
        HTTPException: If task is not found
    """
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    db_task = session.exec(statement).first()

    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    db_task.is_completed = True
    session.add(db_task)
    session.commit()
    session.refresh(db_task)

    return TaskRead.model_validate(db_task.model_dump())