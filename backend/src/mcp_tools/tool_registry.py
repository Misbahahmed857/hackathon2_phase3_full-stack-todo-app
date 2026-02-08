"""
MCP tool registry for managing and accessing MCP tools.

This module provides a centralized registry for MCP tools that the AI agent can use
to perform task operations. It handles tool registration, retrieval, and execution
while maintaining statelessness and using only MCP tools for data access.
"""
from typing import Dict, Any, Callable, Optional
from sqlmodel import Session
from . import mcp_tools_instance


class ToolRegistry:
    """Registry for managing MCP tools."""

    def __init__(self):
        """Initialize the tool registry."""
        self._tools = {}
        self._schemas = {}

    def register_tool(self, name: str, func: Callable, schema: Dict[str, Any]):
        """
        Register an MCP tool with its function and schema.

        Args:
            name: Name of the tool
            func: Function that implements the tool
            schema: JSON schema defining the tool's input parameters
        """
        self._tools[name] = func
        self._schemas[name] = schema

    def get_tool(self, name: str) -> Optional[Callable]:
        """
        Get a registered tool by name.

        Args:
            name: Name of the tool to retrieve

        Returns:
            Tool function or None if not found
        """
        return self._tools.get(name)

    def get_tool_schema(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Get the schema for a registered tool.

        Args:
            name: Name of the tool

        Returns:
            Tool schema or None if not found
        """
        return self._schemas.get(name)

    def get_all_tool_names(self) -> list:
        """
        Get all registered tool names.

        Returns:
            List of all registered tool names
        """
        return list(self._tools.keys())

    def execute_tool(self, name: str, **kwargs) -> Any:
        """
        Execute a registered tool with the given parameters.

        Args:
            name: Name of the tool to execute
            **kwargs: Parameters to pass to the tool

        Returns:
            Result of the tool execution
        """
        tool_func = self.get_tool(name)
        if not tool_func:
            raise ValueError(f"Tool '{name}' not found in registry")

        return tool_func(**kwargs)

    def initialize_default_tools(self, db_session: Session, user_id: str):
        """
        Initialize the default task management tools.

        Args:
            db_session: Database session for data access
            user_id: ID of the user who will use these tools
        """
        from .task_tools import (
            create_add_task_tool,
            create_list_tasks_tool,
            create_complete_task_tool,
            create_update_task_tool,
            create_delete_task_tool
        )

        # Register add_task tool
        add_task_func = create_add_task_tool(db_session, user_id)
        add_task_schema = {
            "name": "add_task",
            "description": "Create a new task",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "The title of the task"
                    },
                    "description": {
                        "type": "string",
                        "description": "Optional description of the task"
                    },
                    "due_date": {
                        "type": "string",
                        "description": "Optional due date for the task in ISO 8601 format"
                    }
                },
                "required": ["title"]
            }
        }
        self.register_tool("add_task", add_task_func, add_task_schema)

        # Register list_tasks tool
        list_tasks_func = create_list_tasks_tool(db_session, user_id)
        list_tasks_schema = {
            "name": "list_tasks",
            "description": "Retrieve tasks based on specified criteria",
            "parameters": {
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "enum": ["all", "pending", "completed"],
                        "default": "all",
                        "description": "Filter tasks by status"
                    },
                    "limit": {
                        "type": "integer",
                        "minimum": 1,
                        "maximum": 100,
                        "description": "Maximum number of tasks to return"
                    }
                }
            }
        }
        self.register_tool("list_tasks", list_tasks_func, list_tasks_schema)

        # Register complete_task tool
        complete_task_func = create_complete_task_tool(db_session, user_id)
        complete_task_schema = {
            "name": "complete_task",
            "description": "Mark a task as completed",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "integer",
                        "description": "The ID of the task to complete"
                    }
                },
                "required": ["task_id"]
            }
        }
        self.register_tool("complete_task", complete_task_func, complete_task_schema)

        # Register update_task tool
        update_task_func = create_update_task_tool(db_session, user_id)
        update_task_schema = {
            "name": "update_task",
            "description": "Update an existing task",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "integer",
                        "description": "The ID of the task to update"
                    },
                    "title": {
                        "type": "string",
                        "description": "The new title for the task (optional)"
                    },
                    "description": {
                        "type": "string",
                        "description": "The new description for the task (optional)"
                    },
                    "due_date": {
                        "type": "string",
                        "description": "The new due date for the task in ISO 8601 format (optional)"
                    }
                },
                "required": ["task_id"]
            }
        }
        self.register_tool("update_task", update_task_func, update_task_schema)

        # Register delete_task tool
        delete_task_func = create_delete_task_tool(db_session, user_id)
        delete_task_schema = {
            "name": "delete_task",
            "description": "Remove a task from the system",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "integer",
                        "description": "The ID of the task to delete"
                    }
                },
                "required": ["task_id"]
            }
        }
        self.register_tool("delete_task", delete_task_func, delete_task_schema)


# Global instance of the tool registry
tool_registry = ToolRegistry()


def get_tool_registry():
    """Get the global tool registry instance."""
    return tool_registry