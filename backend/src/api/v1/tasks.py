from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session
from typing import List
from src.database import engine
from src.services.auth import verify_token
from src.services.tasks import (
    create_task,
    get_tasks_by_user,
    get_task_by_id,
    update_task,
    delete_task
)
from src.models.task import TaskCreate, TaskRead, TaskUpdate, TaskPatch

router = APIRouter()
security = HTTPBearer()


def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """Extract user ID from JWT token"""
    token = credentials.credentials
    payload = verify_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user_id


@router.post("/tasks", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task_endpoint(
    task: TaskCreate,
    user_id: str = Depends(get_current_user_id)
):
    """Create a new task for the authenticated user"""
    with Session(engine) as session:
        return create_task(session=session, task=task, user_id=user_id)


@router.get("/tasks", response_model=List[TaskRead])
def get_tasks_endpoint(user_id: str = Depends(get_current_user_id)):
    """Get all tasks for the authenticated user"""
    with Session(engine) as session:
        return get_tasks_by_user(session=session, user_id=user_id)


@router.get("/tasks/{task_id}", response_model=TaskRead)
def get_task_endpoint(
    task_id: str,
    user_id: str = Depends(get_current_user_id)
):
    """Get a specific task by ID for the authenticated user"""
    with Session(engine) as session:
        return get_task_by_id(session=session, task_id=task_id, user_id=user_id)


@router.put("/tasks/{task_id}", response_model=TaskRead)
def update_task_endpoint(
    task_id: str,
    task_update: TaskUpdate,
    user_id: str = Depends(get_current_user_id)
):
    """Update a specific task for the authenticated user"""
    with Session(engine) as session:
        return update_task(session=session, task_id=task_id, task_update=task_update, user_id=user_id)


@router.patch("/tasks/{task_id}", response_model=TaskRead)
def patch_task_endpoint(
    task_id: str,
    task_patch: TaskPatch,
    user_id: str = Depends(get_current_user_id)
):
    """Partially update a specific task for the authenticated user"""
    with Session(engine) as session:
        # Convert TaskPatch to TaskUpdate for compatibility
        update_data = task_patch.model_dump(exclude_unset=True)
        task_update = TaskUpdate(**update_data)
        return update_task(session=session, task_id=task_id, task_update=task_update, user_id=user_id)


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task_endpoint(
    task_id: str,
    user_id: str = Depends(get_current_user_id)
):
    """Delete a specific task for the authenticated user"""
    with Session(engine) as session:
        success = delete_task(session=session, task_id=task_id, user_id=user_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        return