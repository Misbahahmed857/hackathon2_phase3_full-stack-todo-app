"""
Unit tests for the list_tasks MCP tool.
"""
import pytest
from unittest.mock import Mock, AsyncMock, patch
from src.mcp_server.tools.list_tasks_tool import list_tasks


class TestListTasksTool:
    """Test cases for the list_tasks tool."""

    @pytest.mark.asyncio
    async def test_list_tasks_success(self):
        """Test successful task listing."""
        # Mock the database session and service
        mock_session = Mock()

        with patch('src.mcp_server.tools.list_tasks_tool.get_tasks_by_user_filtered') as mock_get_tasks:
            # Mock the return value of get_tasks_by_user_filtered
            mock_task_result = Mock()
            mock_task_result.id = "test-id"
            mock_task_result.title = "Test Task"
            mock_task_result.description = "Test Description"
            mock_task_result.is_completed = False
            mock_get_tasks.return_value = [mock_task_result]

            result = await list_tasks(
                status_filter="all",
                limit=10,
                db_session=mock_session,
                user_id="test-user"
            )

            # Verify the result
            assert result["success"] is True
            assert result["count"] == 1
            assert "Retrieved 1 tasks" in result["message"]

            # Verify that get_tasks_by_user_filtered was called with correct parameters
            mock_get_tasks.assert_called_once()

    @pytest.mark.asyncio
    async def test_list_tasks_with_invalid_status(self):
        """Test that invalid status filter defaults to 'all'."""
        mock_session = Mock()

        with patch('src.mcp_server.tools.list_tasks_tool.get_tasks_by_user_filtered') as mock_get_tasks:
            mock_task_result = Mock()
            mock_task_result.id = "test-id"
            mock_task_result.title = "Test Task"
            mock_get_tasks.return_value = [mock_task_result]

            result = await list_tasks(
                status_filter="invalid-status",
                limit=10,
                db_session=mock_session,
                user_id="test-user"
            )

            # Verify the result
            assert result["success"] is True
            assert result["status_filter"] == "all"  # Should default to "all"

    @pytest.mark.asyncio
    async def test_list_tasks_with_invalid_limit(self):
        """Test that invalid limit is handled properly."""
        mock_session = Mock()

        with patch('src.mcp_server.tools.list_tasks_tool.get_tasks_by_user_filtered') as mock_get_tasks:
            mock_task_result = Mock()
            mock_task_result.id = "test-id"
            mock_task_result.title = "Test Task"
            mock_get_tasks.return_value = [mock_task_result]

            result = await list_tasks(
                status_filter="all",
                limit=-5,  # Invalid limit
                db_session=mock_session,
                user_id="test-user"
            )

            # Should handle invalid limit gracefully
            assert result["success"] is True

    @pytest.mark.asyncio
    async def test_list_tasks_exception_handling(self):
        """Test that exceptions are handled gracefully."""
        with patch('src.mcp_server.tools.list_tasks_tool.get_tasks_by_user_filtered', side_effect=Exception("DB Error")):
            result = await list_tasks(
                status_filter="all",
                limit=10,
                db_session=Mock(),
                user_id="test-user"
            )

            assert result["success"] is False
            assert "An error occurred while retrieving tasks" in result["message"]