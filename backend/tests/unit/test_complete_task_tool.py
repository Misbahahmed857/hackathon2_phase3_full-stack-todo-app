"""
Unit tests for the complete_task MCP tool.
"""
import pytest
from unittest.mock import Mock, AsyncMock, patch
from src.mcp_server.tools.complete_task_tool import complete_task


class TestCompleteTaskTool:
    """Test cases for the complete_task tool."""

    @pytest.mark.asyncio
    async def test_complete_task_success(self):
        """Test successful task completion."""
        # Mock the database session and service
        mock_session = Mock()

        with patch('src.mcp_server.tools.complete_task_tool.service_complete_task') as mock_complete_task:
            # Mock the return value of service_complete_task
            mock_task_result = Mock()
            mock_task_result.id = "test-id"
            mock_task_result.title = "Test Task"
            mock_task_result.description = "Test Description"
            mock_task_result.is_completed = True
            mock_complete_task.return_value = mock_task_result

            result = await complete_task(
                task_id=123,
                db_session=mock_session,
                user_id="test-user"
            )

            # Verify the result
            assert result["success"] is True
            assert "Successfully marked task" in result["message"]

            # Verify that service_complete_task was called with correct parameters
            mock_complete_task.assert_called_once()

    @pytest.mark.asyncio
    async def test_complete_task_missing_task_id(self):
        """Test that task completion fails when task_id is missing."""
        result = await complete_task(
            task_id=None,  # Missing task_id
            db_session=Mock(),
            user_id="test-user"
        )

        assert result["success"] is False
        assert "Task ID is required" in result["message"]

    @pytest.mark.asyncio
    async def test_complete_task_zero_task_id(self):
        """Test that task completion fails when task_id is zero."""
        result = await complete_task(
            task_id=0,  # Zero task_id
            db_session=Mock(),
            user_id="test-user"
        )

        assert result["success"] is False
        assert "Task ID is required" in result["message"]

    @pytest.mark.asyncio
    async def test_complete_task_exception_handling(self):
        """Test that exceptions are handled gracefully."""
        with patch('src.mcp_server.tools.complete_task_tool.service_complete_task', side_effect=Exception("DB Error")):
            result = await complete_task(
                task_id=123,
                db_session=Mock(),
                user_id="test-user"
            )

            assert result["success"] is False
            assert "An error occurred while completing the task" in result["message"]