"""
Integration tests for the MCP server and its tools.
Tests the full stack of the MCP server including database interactions.
"""
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from unittest.mock import patch
from src.mcp_server.server import app
from src.mcp_server.models.task import Task
from src.mcp_server.database.connection import get_session
import uuid


@pytest.fixture(name="engine")
def fixture_engine():
    """Create an in-memory SQLite database for testing."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(bind=engine)
    return engine


@pytest.fixture(name="session")
def fixture_session(engine):
    """Create a database session for testing."""
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def fixture_client(session):
    """Create a test client for the MCP server."""
    def get_session_override():
        yield session

    app.dependency_overrides[get_session] = get_session_override
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()


class TestMCPServerIntegration:
    """Integration tests for the MCP server endpoints."""

    def test_root_endpoint(self, client):
        """Test the root endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "MCP Task Management Server is running"
        assert data["status"] == "healthy"

    def test_health_endpoint(self, client):
        """Test the health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] in ["healthy", "degraded"]
        assert "database_connected" in data
        assert data["service"] == "mcp-server"

    def test_list_available_tools(self, client):
        """Test the tools listing endpoint."""
        response = client.get("/tools")
        assert response.status_code == 200
        data = response.json()
        assert "tools" in data
        assert "count" in data
        assert data["count"] > 0
        # Check that all expected tools are available
        expected_tools = ["add_task", "list_tasks", "complete_task", "update_task", "delete_task"]
        for tool in expected_tools:
            assert tool in data["tools"]

    def test_add_task_integration(self, client, session):
        """Test adding a task through the MCP server."""
        # Use a fixed user ID for testing
        user_id = "test-user-" + str(uuid.uuid4())

        response = client.post(
            "/tools/add_task",
            params={
                "title": "Test Integration Task",
                "description": "Test description for integration",
                "user_id": user_id
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "task_id" in data
        assert "Successfully created task" in data["message"]

        # Verify the task was actually created in the database
        task_id = data["task_id"]
        task = session.get(Task, task_id)
        assert task is not None
        assert task.title == "Test Integration Task"
        assert task.description == "Test description for integration"
        assert task.is_completed is False
        assert task.user_id == user_id

    def test_list_tasks_integration(self, client, session):
        """Test listing tasks through the MCP server."""
        # First, add a few test tasks
        user_id = "test-user-" + str(uuid.uuid4())

        # Add a pending task
        add_response = client.post(
            "/tools/add_task",
            params={
                "title": "Pending Task",
                "description": "A pending task",
                "user_id": user_id
            }
        )
        assert add_response.status_code == 200

        # Add a completed task
        add_response = client.post(
            "/tools/add_task",
            params={
                "title": "Completed Task",
                "description": "A completed task",
                "user_id": user_id
            }
        )
        assert add_response.status_code == 200
        completed_task_id = add_response.json()["task_id"]

        # Complete the second task
        complete_response = client.post(
            "/tools/complete_task",
            params={
                "task_id": int(completed_task_id),
                "user_id": user_id
            }
        )
        assert complete_response.status_code == 200

        # Test listing all tasks
        list_response = client.post(
            "/tools/list_tasks",
            params={
                "user_id": user_id
            }
        )
        assert list_response.status_code == 200
        data = list_response.json()
        assert data["success"] is True
        assert data["count"] == 2
        assert len(data["tasks"]) == 2

        # Test listing pending tasks only
        list_pending_response = client.post(
            "/tools/list_tasks",
            params={
                "status_filter": "pending",
                "user_id": user_id
            }
        )
        assert list_pending_response.status_code == 200
        pending_data = list_pending_response.json()
        assert pending_data["success"] is True
        assert pending_data["count"] == 1
        assert pending_data["status_filter"] == "pending"
        assert pending_data["tasks"][0]["status"] == "pending"

        # Test listing completed tasks only
        list_completed_response = client.post(
            "/tools/list_tasks",
            params={
                "status_filter": "completed",
                "user_id": user_id
            }
        )
        assert list_completed_response.status_code == 200
        completed_data = list_completed_response.json()
        assert completed_data["success"] is True
        assert completed_data["count"] == 1
        assert completed_data["status_filter"] == "completed"
        assert completed_data["tasks"][0]["status"] == "completed"

    def test_complete_task_integration(self, client, session):
        """Test completing a task through the MCP server."""
        user_id = "test-user-" + str(uuid.uuid4())

        # Add a task first
        add_response = client.post(
            "/tools/add_task",
            params={
                "title": "Task to Complete",
                "description": "This will be completed",
                "user_id": user_id
            }
        )
        assert add_response.status_code == 200
        task_id = add_response.json()["task_id"]

        # Verify task is initially pending
        initial_list_response = client.post(
            "/tools/list_tasks",
            params={
                "status_filter": "pending",
                "user_id": user_id
            }
        )
        assert initial_list_response.status_code == 200
        initial_data = initial_list_response.json()
        assert initial_data["count"] >= 1
        task_found = False
        for task in initial_data["tasks"]:
            if task["id"] == task_id:
                assert task["status"] == "pending"
                task_found = True
                break
        assert task_found

        # Complete the task
        complete_response = client.post(
            "/tools/complete_task",
            params={
                "task_id": int(task_id),
                "user_id": user_id
            }
        )
        assert complete_response.status_code == 200
        complete_data = complete_response.json()
        assert complete_data["success"] is True
        assert "as completed" in complete_data["message"]

        # Verify task is now completed
        completed_list_response = client.post(
            "/tools/list_tasks",
            params={
                "status_filter": "completed",
                "user_id": user_id
            }
        )
        assert completed_list_response.status_code == 200
        completed_data = completed_list_response.json()
        assert completed_data["count"] >= 1
        task_found = False
        for task in completed_data["tasks"]:
            if task["id"] == task_id:
                assert task["status"] == "completed"
                task_found = True
                break
        assert task_found

    def test_update_task_integration(self, client, session):
        """Test updating a task through the MCP server."""
        user_id = "test-user-" + str(uuid.uuid4())

        # Add a task first
        add_response = client.post(
            "/tools/add_task",
            params={
                "title": "Original Title",
                "description": "Original Description",
                "user_id": user_id
            }
        )
        assert add_response.status_code == 200
        task_id = add_response.json()["task_id"]

        # Update the task
        update_response = client.post(
            "/tools/update_task",
            params={
                "task_id": int(task_id),
                "title": "Updated Title",
                "description": "Updated Description",
                "user_id": user_id
            }
        )
        assert update_response.status_code == 200
        update_data = update_response.json()
        assert update_data["success"] is True
        assert "Successfully updated task" in update_data["message"]

        # Verify the update worked
        list_response = client.post(
            "/tools/list_tasks",
            params={
                "user_id": user_id
            }
        )
        assert list_response.status_code == 200
        list_data = list_response.json()

        task_found = False
        for task in list_data["tasks"]:
            if task["id"] == task_id:
                assert task["title"] == "Updated Title"
                assert task["description"] == "Updated Description"
                task_found = True
                break
        assert task_found

    def test_delete_task_integration(self, client, session):
        """Test deleting a task through the MCP server."""
        user_id = "test-user-" + str(uuid.uuid4())

        # Add a task first
        add_response = client.post(
            "/tools/add_task",
            params={
                "title": "Task to Delete",
                "description": "This will be deleted",
                "user_id": user_id
            }
        )
        assert add_response.status_code == 200
        task_id = add_response.json()["task_id"]

        # Verify task exists before deletion
        list_before_response = client.post(
            "/tools/list_tasks",
            params={
                "user_id": user_id
            }
        )
        assert list_before_response.status_code == 200
        before_data = list_before_response.json()
        assert before_data["count"] >= 1
        task_exists_before = any(task["id"] == task_id for task in before_data["tasks"])
        assert task_exists_before

        # Delete the task
        delete_response = client.post(
            "/tools/delete_task",
            params={
                "task_id": int(task_id),
                "user_id": user_id
            }
        )
        assert delete_response.status_code == 200
        delete_data = delete_response.json()
        assert delete_data["success"] is True
        assert "Successfully deleted" in delete_data["message"]

        # Verify task no longer exists
        list_after_response = client.post(
            "/tools/list_tasks",
            params={
                "user_id": user_id
            }
        )
        assert list_after_response.status_code == 200
        after_data = list_after_response.json()

        task_exists_after = any(task["id"] == task_id for task in after_data["tasks"])
        assert not task_exists_after

    def test_error_scenarios_integration(self, client):
        """Test error scenarios in the MCP server."""
        user_id = "test-user-" + str(uuid.uuid4())

        # Test adding a task without title
        response = client.post(
            "/tools/add_task",
            params={
                "title": "",  # Empty title
                "user_id": user_id
            }
        )
        assert response.status_code == 500  # FastAPI raises 500 for internal errors