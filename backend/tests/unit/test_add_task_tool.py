"""
Unit tests for the add_task MCP tool.
"""
import pytest
from unittest.mock import Mock, AsyncMock, patch
from src.mcp_server.tools.add_task_tool import add_task


class TestAddTaskTool:
    """Test cases for the add_task tool."""

    @pytest.mark.asyncio
    async def test_add_task_success(self):
        """Test successful task creation."""
        # Mock the database session and service
        mock_session = Mock()

        with patch('src.mcp_server.tools.add_task_tool.create_task') as mock_create_task:
            # Mock the return value of create_task
            mock_task_result = Mock()
            mock_task_result.id = "test-id"
            mock_task_result.title = "Test Task"
            mock_task_result.description = "Test Description"
            mock_task_result.is_completed = False
            mock_create_task.return_value = mock_task_result

            result = await add_task(
                title="Test Task",
                description="Test Description",
                db_session=mock_session,
                user_id="test-user"
            )

            # Verify the result
            assert result["success"] is True
            assert result["task_id"] == "test-id"
            assert "Successfully created task" in result["message"]

            # Verify that create_task was called with correct parameters
            mock_create_task.assert_called_once()

    @pytest.mark.asyncio
    async def test_add_task_missing_title(self):
        """Test that task creation fails when title is missing."""
        result = await add_task(
            title="",  # Empty title
            description="Test Description",
            db_session=Mock(),
            user_id="test-user"
        )

        assert result["success"] is False
        assert "Title is required" in result["message"]

    @pytest.mark.asyncio
    async def test_add_task_whitespace_title(self):
        """Test that task creation fails when title contains only whitespace."""
        result = await add_task(
            title="   ",  # Whitespace-only title
            description="Test Description",
            db_session=Mock(),
            user_id="test-user"
        )

        assert result["success"] is False
        assert "Title is required" in result["message"]

    @pytest.mark.asyncio
    async def test_add_task_exception_handling(self):
        """Test that exceptions are handled gracefully."""
        with patch('src.mcp_server.tools.add_task_tool.create_task', side_effect=Exception("DB Error")):
            result = await add_task(
                title="Test Task",
                description="Test Description",
                db_session=Mock(),
                user_id="test-user"
            )

            assert result["success"] is False
            assert "An error occurred while creating the task" in result["message"]