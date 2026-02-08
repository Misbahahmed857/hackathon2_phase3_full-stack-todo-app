"""
Shared schemas for MCP tools in the task management system.

This module defines the JSON schemas for all MCP tools used by the task management
server, ensuring consistent input and output formats across all tools.
"""
from typing import Dict, Any


def get_add_task_schema() -> Dict[str, Any]:
    """
    Get the schema for the add_task MCP tool.

    Returns:
        Dict: JSON schema for add_task tool
    """
    return {
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
                    "format": "date-time",
                    "description": "Optional due date for the task in ISO 8601 format"
                }
            },
            "required": ["title"]
        }
    }


def get_list_tasks_schema() -> Dict[str, Any]:
    """
    Get the schema for the list_tasks MCP tool.

    Returns:
        Dict: JSON schema for list_tasks tool
    """
    return {
        "name": "list_tasks",
        "description": "Retrieves tasks based on specified criteria",
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


def get_complete_task_schema() -> Dict[str, Any]:
    """
    Get the schema for the complete_task MCP tool.

    Returns:
        Dict: JSON schema for complete_task tool
    """
    return {
        "name": "complete_task",
        "description": "Marks a task as completed",
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


def get_update_task_schema() -> Dict[str, Any]:
    """
    Get the schema for the update_task MCP tool.

    Returns:
        Dict: JSON schema for update_task tool
    """
    return {
        "name": "update_task",
        "description": "Updates an existing task",
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
                    "format": "date-time",
                    "description": "The new due date for the task in ISO 8601 format (optional)"
                }
            },
            "required": ["task_id"]
        }
    }


def get_delete_task_schema() -> Dict[str, Any]:
    """
    Get the schema for the delete_task MCP tool.

    Returns:
        Dict: JSON schema for delete_task tool
    """
    return {
        "name": "delete_task",
        "description": "Removes a task from the system",
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


def get_all_tool_schemas() -> Dict[str, Dict[str, Any]]:
    """
    Get all tool schemas in a single dictionary.

    Returns:
        Dict: Dictionary containing all tool schemas keyed by name
    """
    return {
        "add_task": get_add_task_schema(),
        "list_tasks": get_list_tasks_schema(),
        "complete_task": get_complete_task_schema(),
        "update_task": get_update_task_schema(),
        "delete_task": get_delete_task_schema()
    }