from sqlmodel import Session, select
from typing import List, Optional
from src.models.task import Task, TaskCreate, TaskUpdate, TaskRead
from fastapi import HTTPException, status


def create_task(*, session: Session, task: TaskCreate, user_id: str) -> TaskRead:
    """Create a new task for the authenticated user"""
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
    """Get all tasks for the authenticated user"""
    statement = select(Task).where(Task.user_id == user_id)
    tasks = session.exec(statement).all()

    return [TaskRead.model_validate(task.model_dump()) for task in tasks]


def get_task_by_id(*, session: Session, task_id: str, user_id: str) -> TaskRead:
    """Get a specific task by ID for the authenticated user"""
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    db_task = session.exec(statement).first()

    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return TaskRead.model_validate(db_task.model_dump())


def update_task(*, session: Session, task_id: str, task_update: TaskUpdate, user_id: str) -> TaskRead:
    """Update a specific task for the authenticated user"""
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
    """Delete a specific task for the authenticated user"""
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