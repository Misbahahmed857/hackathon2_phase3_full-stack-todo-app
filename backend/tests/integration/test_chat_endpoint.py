"""
Integration tests for the chat endpoint.
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from src.main import app
from src.database import engine
from sqlmodel import SQLModel, Session, select
from src.models.user import User
from src.models.task import Task
from src.services.auth import create_access_token
from uuid import uuid4


@pytest.fixture
def client():
    """Create a test client for the API."""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def mock_user():
    """Create a mock user for testing."""
    user = User(
        id=str(uuid4()),
        email="test@example.com",
        hashed_password="hashed_test_password",
        is_active=True
    )
    return user


@pytest.fixture
def auth_headers(mock_user):
    """Create authentication headers for testing."""
    token = create_access_token(data={"sub": mock_user.email})
    return {"Authorization": f"Bearer {token}"}


class TestChatEndpoint:
    """Test cases for the chat endpoint."""

    def test_chat_message_unauthorized(self, client):
        """Test that chat endpoint requires authentication."""
        response = client.post("/chat/message", json={"message": "Hello"})

        # Should return 401 or 403 for unauthorized access
        assert response.status_code in [401, 403]

    @patch('src.agents.ai_agent.AIAgent')
    def test_chat_message_authorized(self, mock_agent_class, client, auth_headers):
        """Test that chat endpoint works with authentication."""
        # Mock the AI agent
        mock_agent_instance = mock_agent_class.return_value
        mock_agent_instance.process_request.return_value = "Test response from AI agent"

        # Make a request to the chat endpoint
        response = client.post(
            "/chat/message",
            json={"message": "Add a task to buy groceries"},
            headers=auth_headers
        )

        # Should return 200 for successful request
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["response"] == "Test response from AI agent"
        assert response_data["success"] is True

    def test_chat_health_check(self, client):
        """Test the health check endpoint."""
        response = client.get("/chat/health")

        assert response.status_code == 200
        response_data = response.json()
        assert response_data["status"] == "healthy"
        assert response_data["service"] == "chat"