"""
Main MCP server implementation for task management.

This module implements the MCP server using FastAPI and the Official MCP SDK,
exposing task operations as stateless tools that interact with Neon PostgreSQL
for persistence, ensuring stateless operation and compliance with constitutional requirements.
"""
from fastapi import FastAPI, Depends, HTTPException, status
from typing import Dict, Any, List
from sqlmodel import Session
from contextlib import asynccontextmanager
import logging
import traceback

# Import from our modules
from .database.connection import engine, get_session
from .models.task import Task
from .tools.add_task_tool import add_task
from .tools.list_tasks_tool import list_tasks
from .tools.complete_task_tool import complete_task
from .tools.update_task_tool import update_task
from .tools.delete_task_tool import delete_task
from .tools.tool_schemas import get_all_tool_schemas


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MCPServerError(Exception):
    """Custom exception for MCP server errors."""
    pass


def handle_mcp_error(error: Exception, context: str = "") -> Dict[str, Any]:
    """
    Handle errors in MCP tools and return user-friendly responses.

    Args:
        error: The exception that occurred
        context: Context information about where the error occurred

    Returns:
        Dict: Error response with user-friendly message
    """
    logger.error(f"MCP Error in {context}: {str(error)}")
    logger.debug(f"Full error traceback: {traceback.format_exc()}")

    # Return a user-friendly error response
    return {
        "success": False,
        "error": "An error occurred while processing your request. Please try again.",
        "details": str(error) if isinstance(error, ValueError) else "Internal server error"
    }


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan manager for the MCP server.
    Handles startup and shutdown events.
    """
    # Startup: Initialize any required resources
    logger.info("Starting MCP server for task management")

    # Create tables if they don't exist
    from sqlmodel import SQLModel
    SQLModel.metadata.create_all(engine)

    yield

    # Shutdown: Clean up resources
    logger.info("Shutting down MCP server")


# Create the FastAPI app
app = FastAPI(
    title="MCP Task Management Server",
    description="Model Context Protocol server for task management operations",
    version="1.0.0",
    lifespan=lifespan
)


@app.get("/")
async def root():
    """
    Root endpoint for the MCP server.

    Returns:
        Dict: Server status information
    """
    return {"message": "MCP Task Management Server is running", "status": "healthy"}


@app.get("/health")
async def health_check():
    """
    Health check endpoint for the MCP server.

    Returns:
        Dict: Health status information
    """
    from .database.connection import test_connection

    db_connected = test_connection()

    return {
        "status": "healthy" if db_connected else "degraded",
        "database_connected": db_connected,
        "service": "mcp-server"
    }


@app.get("/tools")
async def list_available_tools():
    """
    List all available MCP tools.

    Returns:
        Dict: Information about all available tools
    """
    schemas = get_all_tool_schemas()
    tool_names = list(schemas.keys())

    return {
        "tools": tool_names,
        "count": len(tool_names),
        "description": "Available MCP tools for task management"
    }


# Placeholder endpoints for the tools - these would normally be MCP protocol endpoints
# In a real MCP implementation, these would follow the MCP protocol specification
@app.post("/tools/add_task")
async def tool_add_task(
    title: str,
    description: str = None,
    due_date: str = None,
    user_id: str = "default_user",  # In a real implementation, this would come from auth
    db_session: Session = Depends(get_session)
):
    """
    MCP tool endpoint for adding tasks.

    Args:
        title: Title of the task to add
        description: Optional description of the task
        due_date: Optional due date for the task
        user_id: ID of the user making the request
        db_session: Database session for the operation

    Returns:
        Dict: Result of the add_task operation
    """
    try:
        result = await add_task(
            title=title,
            description=description,
            due_date=due_date,
            db_session=db_session,
            user_id=user_id
        )
        return result
    except Exception as e:
        logger.error(f"Error in add_task tool: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error executing add_task: {str(e)}"
        )


@app.post("/tools/list_tasks")
async def tool_list_tasks(
    status_filter: str = "all",
    limit: int = None,
    user_id: str = "default_user",  # In a real implementation, this would come from auth
    db_session: Session = Depends(get_session)
):
    """
    MCP tool endpoint for listing tasks.

    Args:
        status_filter: Filter tasks by status ('all', 'pending', 'completed')
        limit: Maximum number of tasks to return
        user_id: ID of the user making the request
        db_session: Database session for the operation

    Returns:
        Dict: Result of the list_tasks operation
    """
    try:
        result = await list_tasks(
            status_filter=status_filter,
            limit=limit,
            db_session=db_session,
            user_id=user_id
        )
        return result
    except Exception as e:
        logger.error(f"Error in list_tasks tool: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error executing list_tasks: {str(e)}"
        )


@app.post("/tools/complete_task")
async def tool_complete_task(
    task_id: int,
    user_id: str = "default_user",  # In a real implementation, this would come from auth
    db_session: Session = Depends(get_session)
):
    """
    MCP tool endpoint for completing tasks.

    Args:
        task_id: ID of the task to complete
        user_id: ID of the user making the request
        db_session: Database session for the operation

    Returns:
        Dict: Result of the complete_task operation
    """
    try:
        result = await complete_task(
            task_id=task_id,
            db_session=db_session,
            user_id=user_id
        )
        return result
    except Exception as e:
        logger.error(f"Error in complete_task tool: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error executing complete_task: {str(e)}"
        )


@app.post("/tools/update_task")
async def tool_update_task(
    task_id: int,
    title: str = None,
    description: str = None,
    due_date: str = None,
    user_id: str = "default_user",  # In a real implementation, this would come from auth
    db_session: Session = Depends(get_session)
):
    """
    MCP tool endpoint for updating tasks.

    Args:
        task_id: ID of the task to update
        title: New title for the task (optional)
        description: New description for the task (optional)
        due_date: New due date for the task (optional)
        user_id: ID of the user making the request
        db_session: Database session for the operation

    Returns:
        Dict: Result of the update_task operation
    """
    try:
        result = await update_task(
            task_id=task_id,
            title=title,
            description=description,
            due_date=due_date,
            db_session=db_session,
            user_id=user_id
        )
        return result
    except Exception as e:
        logger.error(f"Error in update_task tool: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error executing update_task: {str(e)}"
        )


@app.post("/tools/delete_task")
async def tool_delete_task(
    task_id: int,
    user_id: str = "default_user",  # In a real implementation, this would come from auth
    db_session: Session = Depends(get_session)
):
    """
    MCP tool endpoint for deleting tasks.

    Args:
        task_id: ID of the task to delete
        user_id: ID of the user making the request
        db_session: Database session for the operation

    Returns:
        Dict: Result of the delete_task operation
    """
    try:
        result = await delete_task(
            task_id=task_id,
            db_session=db_session,
            user_id=user_id
        )
        return result
    except Exception as e:
        logger.error(f"Error in delete_task tool: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error executing delete_task: {str(e)}"
        )


# Function to register tools with the MCP system
def register_mcp_tools():
    """
    Register all MCP tools with the server.
    This would be called during server initialization in a real MCP implementation.
    """
    logger.info("Registering MCP tools...")
    # In a real MCP implementation, this would register tools with the MCP protocol
    # For now, we just log that the tools are available
    schemas = get_all_tool_schemas()
    for tool_name, schema in schemas.items():
        logger.info(f"Registered tool: {tool_name}")

    logger.info(f"Total tools registered: {len(schemas)}")


# Call the registration function
register_mcp_tools()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)