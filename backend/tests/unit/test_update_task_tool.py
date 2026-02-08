"""
Unit tests for the update_task MCP tool.
"""
import pytest
from unittest.mock import Mock, AsyncMock, patch
from src.mcp_server.tools.update_task_tool import update_task


class TestUpdateTaskTool:
    """Test cases for the update_task tool."""

    @pytest.mark.asyncio
    async def test_update_task_success(self):
        """Test successful task update."""
        # Mock the database session and service
        mock_session = Mock()

        with patch('src.mcp_server.tools.update_task_tool.service_update_task') as mock_update_task:
            # Mock the return value of service_update_task
            mock_task_result = Mock()
            mock_task_result.id = "test-id"
            mock_task_result.title = "Updated Task"
            mock_task_result.description = "Updated Description"
            mock_task_result.is_completed = False
            mock_update_task.return_value = mock_task_result

            result = await update_task(
                task_id=123,
                title="Updated Task",
                description="Updated Description",
                db_session=mock_session,
                user_id="test-user"
            )

            # Verify the result
            assert result["success"] is True
            assert "Successfully updated task" in result["message"]

            # Verify that service_update_task was called with correct parameters
            mock_update_task.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_task_missing_task_id(self):
        """Test that task update fails when task_id is missing."""
        result = await update_task(
            task_id=None,  # Missing task_id
            title="Updated Task",
            description="Updated Description",
            db_session=Mock(),
            user_id="test-user"
        )

        assert result["success"] is False
        assert "Task ID is required" in result["message"]

    @pytest.mark.asyncio
    async def test_update_task_partial_updates(self):
        """Test that partial updates work correctly."""
        mock_session = Mock()

        with patch('src.mcp_server.tools.update_task_tool.service_update_task') as mock_update_task:
            mock_task_result = Mock()
            mock_task_result.id = "test-id"
            mock_task_result.title = "Partially Updated Task"
            mock_task_result.description = "Original Description"
            mock_task_result.is_completed = False
            mock_update_task.return_value = mock_task_result

            # Update only the title, leave description unchanged
            result = await update_task(
                task_id=123,
                title="Partially Updated Task",
                # No description provided
                db_session=mock_session,
                user_id="test-user"
            )

            # Verify the result
            assert result["success"] is True
            assert "Successfully updated task" in result["message"]

    @pytest.mark.asyncio
    async def test_update_task_exception_handling(self):
        """Test that exceptions are handled gracefully."""
        with patch('src.mcp_server.tools.update_task_tool.service_update_task', side_effect=Exception("DB Error")):
            result = await update_task(
                task_id=123,
                title="Updated Task",
                description="Updated Description",
                db_session=Mock(),
                user_id="test-user"
            )

            assert result["success"] is False
            assert "An error occurred while updating the task" in result["message"]