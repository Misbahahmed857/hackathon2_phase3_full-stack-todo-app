"""
Unit tests for the delete_task MCP tool.
"""
import pytest
from unittest.mock import Mock, AsyncMock, patch
from src.mcp_server.tools.delete_task_tool import delete_task


class TestDeleteTaskTool:
    """Test cases for the delete_task tool."""

    @pytest.mark.asyncio
    async def test_delete_task_success(self):
        """Test successful task deletion."""
        # Mock the database session and service
        mock_session = Mock()

        with patch('src.mcp_server.tools.delete_task_tool.service_delete_task') as mock_delete_task:
            # Mock the return value of service_delete_task
            mock_delete_task.return_value = True

            result = await delete_task(
                task_id=123,
                db_session=mock_session,
                user_id="test-user"
            )

            # Verify the result
            assert result["success"] is True
            assert "Successfully deleted the task" in result["message"]

            # Verify that service_delete_task was called with correct parameters
            mock_delete_task.assert_called_once()

    @pytest.mark.asyncio
    async def test_delete_task_missing_task_id(self):
        """Test that task deletion fails when task_id is missing."""
        result = await delete_task(
            task_id=None,  # Missing task_id
            db_session=Mock(),
            user_id="test-user"
        )

        assert result["success"] is False
        assert "Task ID is required" in result["message"]

    @pytest.mark.asyncio
    async def test_delete_task_zero_task_id(self):
        """Test that task deletion fails when task_id is zero."""
        result = await delete_task(
            task_id=0,  # Zero task_id
            db_session=Mock(),
            user_id="test-user"
        )

        assert result["success"] is False
        assert "Task ID is required" in result["message"]

    @pytest.mark.asyncio
    async def test_delete_task_exception_handling(self):
        """Test that exceptions are handled gracefully."""
        with patch('src.mcp_server.tools.delete_task_tool.service_delete_task', side_effect=Exception("DB Error")):
            result = await delete_task(
                task_id=123,
                db_session=Mock(),
                user_id="test-user"
            )

            assert result["success"] is False
            assert "An error occurred while deleting the task" in result["message"]