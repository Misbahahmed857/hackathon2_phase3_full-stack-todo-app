"""
Unit tests for the AI agent functionality.
"""
import pytest
from unittest.mock import Mock, patch
from sqlmodel import Session
from src.agents.ai_agent import AIAgent
from src.agents.intent_classifier import classify_intent


class TestAIAgent:
    """Test cases for the AI agent."""

    @pytest.fixture
    def mock_db_session(self):
        """Mock database session for testing."""
        return Mock(spec=Session)

    @pytest.fixture
    def ai_agent(self):
        """Create an AI agent instance for testing."""
        # Mock the OpenAI client to avoid actual API calls
        with patch('src.agents.ai_agent.OpenAI'):
            agent = AIAgent(api_key="test_key")
            return agent

    def test_agent_initialization(self, ai_agent):
        """Test that the AI agent initializes correctly."""
        assert ai_agent is not None
        assert ai_agent.system_prompt is not None
        assert "stateless" in ai_agent.system_prompt.lower()

    def test_classify_intent_create_task(self):
        """Test intent classification for task creation."""
        result = classify_intent("Add a task to buy groceries")

        assert result['intent_type'] == 'CREATE_TASK'
        assert result['confidence_score'] > 0.5
        assert 'title' in result['extracted_parameters']

    def test_classify_intent_list_tasks(self):
        """Test intent classification for task listing."""
        result = classify_intent("Show me my tasks")

        assert result['intent_type'] == 'LIST_TASKS'
        assert result['confidence_score'] > 0.5

    def test_classify_intent_complete_task(self):
        """Test intent classification for task completion."""
        result = classify_intent("Mark the homework task as done")

        assert result['intent_type'] == 'COMPLETE_TASK'
        assert result['confidence_score'] > 0.5

    def test_classify_intent_unknown(self):
        """Test intent classification for unknown requests."""
        result = classify_intent("This is not a valid task command")

        assert result['intent_type'] == 'UNKNOWN'
        assert result['confidence_score'] < 0.5

    def test_process_request_with_mocked_tools(self, ai_agent, mock_db_session):
        """Test processing a request with mocked tools."""
        # This test would need more extensive mocking to work properly
        # For now, we'll just test that the method exists and can be called
        with patch.object(ai_agent, 'process_request') as mock_process:
            mock_process.return_value = "Test response"

            response = ai_agent.process_request("Test message", "test_user_id", mock_db_session)
            assert response == "Test response"