import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
import sys
import os
# Add the parent directory to path to import properly
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from backend.src.main import app
from backend.src.models.user import User
from backend.src.models.task import Task
from backend.src.services.auth import create_access_token
from uuid import uuid4


@pytest.fixture(name="engine")
def engine_fixture():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    return engine


@pytest.fixture(name="client")
def client_fixture():
    with TestClient(app) as client:
        yield client


@pytest.fixture(name="test_user")
def test_user_fixture():
    # Create a mock user for testing
    user = User(
        id=str(uuid4()),
        email="test@example.com",
        hashed_password="fake_hashed_password"
    )
    return user


@pytest.fixture(name="auth_headers")
def auth_headers_fixture(test_user):
    access_token = create_access_token(data={"sub": test_user.id, "email": test_user.email})
    return {"Authorization": f"Bearer {access_token}"}


def test_create_task(client: TestClient, auth_headers: dict):
    """Test creating a task for the authenticated user"""
    response = client.post(
        "/api/v1/tasks",
        json={"title": "Test task", "description": "Test description"},
        headers=auth_headers
    )

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test task"
    assert data["description"] == "Test description"
    assert data["is_completed"] is False
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


def test_get_tasks(client: TestClient, auth_headers: dict):
    """Test getting tasks for the authenticated user"""
    # Create a task first
    client.post(
        "/api/v1/tasks",
        json={"title": "Test task", "description": "Test description"},
        headers=auth_headers
    )

    response = client.get("/api/v1/tasks", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1  # At least one task should be present
    assert any(task["title"] == "Test task" for task in data)


def test_get_single_task(client: TestClient, auth_headers: dict):
    """Test getting a single task for the authenticated user"""
    # Create a task first
    create_response = client.post(
        "/api/v1/tasks",
        json={"title": "Test task", "description": "Test description"},
        headers=auth_headers
    )

    if create_response.status_code == 201:
        task_id = create_response.json()["id"]
        response = client.get(f"/api/v1/tasks/{task_id}", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Test task"


def test_update_task(client: TestClient, auth_headers: dict):
    """Test updating a task for the authenticated user"""
    # Create a task first
    create_response = client.post(
        "/api/v1/tasks",
        json={"title": "Test task", "description": "Test description"},
        headers=auth_headers
    )

    if create_response.status_code == 201:
        task_id = create_response.json()["id"]
        response = client.put(
            f"/api/v1/tasks/{task_id}",
            json={"title": "Updated task", "description": "Updated description", "is_completed": True},
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated task"
        assert data["description"] == "Updated description"
        assert data["is_completed"] is True


def test_delete_task(client: TestClient, auth_headers: dict):
    """Test deleting a task for the authenticated user"""
    # Create a task first
    create_response = client.post(
        "/api/v1/tasks",
        json={"title": "Test task", "description": "Test description"},
        headers=auth_headers
    )

    if create_response.status_code == 201:
        task_id = create_response.json()["id"]
        response = client.delete(f"/api/v1/tasks/{task_id}", headers=auth_headers)

        assert response.status_code == 204

        # Verify the task is deleted
        get_response = client.get(f"/api/v1/tasks/{task_id}", headers=auth_headers)
        assert get_response.status_code == 404


def test_validation_rules(client: TestClient, auth_headers: dict):
    """Test validation rules for task creation"""
    # Test title too short
    response = client.post(
        "/api/v1/tasks",
        json={"title": "", "description": "Test description"},
        headers=auth_headers
    )

    assert response.status_code == 422

    # Test title too long
    long_title = "a" * 201
    response = client.post(
        "/api/v1/tasks",
        json={"title": long_title, "description": "Test description"},
        headers=auth_headers
    )

    assert response.status_code == 422

    # Test description too long
    long_description = "a" * 1001
    response = client.post(
        "/api/v1/tasks",
        json={"title": "Valid title", "description": long_description},
        headers=auth_headers
    )

    assert response.status_code == 422