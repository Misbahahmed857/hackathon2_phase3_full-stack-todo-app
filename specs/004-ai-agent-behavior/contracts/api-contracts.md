# API Contract: AI Agent & Behavioral Logic

## Overview
This document defines the API contracts for the conversational AI agent that manages user todos through natural language using the OpenAI Agents SDK, while interacting only through MCP tools.

## MCP Tool Contracts

### add_task
**Purpose**: Creates a new task in the system

**Input Schema**:
```json
{
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
```

**Output Schema**:
```json
{
  "type": "object",
  "properties": {
    "success": {
      "type": "boolean",
      "description": "Indicates if the operation was successful"
    },
    "task_id": {
      "type": "integer",
      "description": "The ID of the created task"
    },
    "message": {
      "type": "string",
      "description": "A confirmation message"
    }
  }
}
```

### list_tasks
**Purpose**: Retrieves tasks based on specified criteria

**Input Schema**:
```json
{
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
```

**Output Schema**:
```json
{
  "type": "object",
  "properties": {
    "success": {
      "type": "boolean",
      "description": "Indicates if the operation was successful"
    },
    "tasks": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "id": {
            "type": "integer",
            "description": "The task ID"
          },
          "title": {
            "type": "string",
            "description": "The task title"
          },
          "description": {
            "type": "string",
            "description": "The task description"
          },
          "status": {
            "type": "string",
            "enum": ["pending", "completed"],
            "description": "The task status"
          },
          "due_date": {
            "type": "string",
            "format": "date-time",
            "description": "The task due date in ISO 8601 format"
          }
        }
      }
    }
  }
}
```

### complete_task
**Purpose**: Marks a task as completed

**Input Schema**:
```json
{
  "type": "object",
  "properties": {
    "task_id": {
      "type": "integer",
      "description": "The ID of the task to complete"
    }
  },
  "required": ["task_id"]
}
```

**Output Schema**:
```json
{
  "type": "object",
  "properties": {
    "success": {
      "type": "boolean",
      "description": "Indicates if the operation was successful"
    },
    "message": {
      "type": "string",
      "description": "A confirmation message"
    }
  }
}
```

### update_task
**Purpose**: Updates an existing task

**Input Schema**:
```json
{
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
```

**Output Schema**:
```json
{
  "type": "object",
  "properties": {
    "success": {
      "type": "boolean",
      "description": "Indicates if the operation was successful"
    },
    "message": {
      "type": "string",
      "description": "A confirmation message"
    }
  }
}
```

### delete_task
**Purpose**: Removes a task from the system

**Input Schema**:
```json
{
  "type": "object",
  "properties": {
    "task_id": {
      "type": "integer",
      "description": "The ID of the task to delete"
    }
  },
  "required": ["task_id"]
}
```

**Output Schema**:
```json
{
  "type": "object",
  "properties": {
    "success": {
      "type": "boolean",
      "description": "Indicates if the operation was successful"
    },
    "message": {
      "type": "string",
      "description": "A confirmation message"
    }
  }
}
```