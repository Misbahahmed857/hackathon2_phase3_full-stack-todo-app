# MCP Task Management Server

The MCP Task Management Server is a Model Context Protocol server for task management operations that exposes task operations as stateless tools interacting with Neon PostgreSQL for persistence.

## Available Tools

### 1. add_task
- **Endpoint**: `POST /tools/add_task`
- **Description**: Create a new task
- **Parameters**:
  - `title` (string, required): The title of the task
  - `description` (string, optional): Optional description of the task
  - `due_date` (string, optional): Optional due date for the task in ISO 8601 format
  - `user_id` (string, optional): ID of the user making the request (defaults to "default_user")
- **Response**:
  - `success` (boolean): Whether the operation was successful
  - `task_id` (string): The ID of the created task
  - `message` (string): Success/error message
  - `task` (object): Task details

### 2. list_tasks
- **Endpoint**: `POST /tools/list_tasks`
- **Description**: Retrieves tasks based on specified criteria
- **Parameters**:
  - `status_filter` (string, optional): Filter tasks by status ("all", "pending", "completed"; defaults to "all")
  - `limit` (integer, optional): Maximum number of tasks to return
  - `user_id` (string, optional): ID of the user making the request (defaults to "default_user")
- **Response**:
  - `success` (boolean): Whether the operation was successful
  - `count` (integer): Number of tasks returned
  - `status_filter` (string): Status filter applied
  - `tasks` (array): Array of task objects
  - `message` (string): Success/error message

### 3. complete_task
- **Endpoint**: `POST /tools/complete_task`
- **Description**: Marks a task as completed
- **Parameters**:
  - `task_id` (string): The ID of the task to complete
  - `user_id` (string, optional): ID of the user making the request (defaults to "default_user")
- **Response**:
  - `success` (boolean): Whether the operation was successful
  - `message` (string): Success/error message
  - `task` (object): Updated task details

### 4. update_task
- **Endpoint**: `POST /tools/update_task`
- **Description**: Updates an existing task
- **Parameters**:
  - `task_id` (string): The ID of the task to update
  - `title` (string, optional): The new title for the task
  - `description` (string, optional): The new description for the task
  - `due_date` (string, optional): The new due date for the task in ISO 8601 format
  - `user_id` (string, optional): ID of the user making the request (defaults to "default_user")
- **Response**:
  - `success` (boolean): Whether the operation was successful
  - `message` (string): Success/error message
  - `task` (object): Updated task details

### 5. delete_task
- **Endpoint**: `POST /tools/delete_task`
- **Description**: Removes a task from the system
- **Parameters**:
  - `task_id` (string): The ID of the task to delete
  - `user_id` (string, optional): ID of the user making the request (defaults to "default_user")
- **Response**:
  - `success` (boolean): Whether the operation was successful
  - `message` (string): Success/error message

## Additional Endpoints

### Root Endpoint
- **Endpoint**: `GET /`
- **Description**: Root endpoint for the MCP server
- **Response**: Server status information

### Health Check
- **Endpoint**: `GET /health`
- **Description**: Health check endpoint for the MCP server
- **Response**: Health status information

### List Available Tools
- **Endpoint**: `GET /tools`
- **Description**: List all available MCP tools
- **Response**: Information about all available tools

## Architecture

The MCP server follows a modular architecture:

- **Models**: Defined in `src/mcp_server/models/` - Contains the Task data model
- **Services**: Defined in `src/mcp_server/services/` - Contains business logic for task operations
- **Tools**: Defined in `src/mcp_server/tools/` - Contains the MCP tool implementations
- **Database**: Defined in `src/mcp_server/database/` - Contains database connection management
- **Server**: Defined in `src/mcp_server/server.py` - Main server implementation

## Configuration

The server uses environment variables for database configuration:
- `DATABASE_URL`: Database connection URL (defaults to SQLite for development)

## Testing

Unit tests are located in `tests/unit/` and integration tests in `tests/integration/`.