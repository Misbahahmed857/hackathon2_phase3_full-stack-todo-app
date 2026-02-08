"""
Main conversational AI agent implementation for task management.

This module implements a stateless conversational AI agent that interprets user intent
and invokes MCP tools using the OpenAI Agents SDK. The agent handles natural language
task management (create, read, update, delete, list) while maintaining strict
statelessness and using only MCP tools for data access.
"""
import os
import logging
from typing import Dict, Any, Optional
from sqlmodel import Session
from openai import OpenAI


# Import logger from the module
logger = logging.getLogger(__name__)


class AIAgent:
    """Conversational AI agent for task management."""

    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        """
        Initialize the AI agent.

        Args:
            api_key: API key. If not provided, will use OPENROUTER_API_KEY env var.
            base_url: Base URL for the API. Defaults to OpenRouter if not provided.
        """
        api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise ValueError("API key must be provided either as parameter or in OPENROUTER_API_KEY environment variable")

        # Set default base URL to OpenRouter if not provided
        base_url = base_url or os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )

        # Define the system prompt for stateless operation
        self.system_prompt = """You are a helpful task management assistant. You help users manage their tasks through natural language.

        IMPORTANT RULES:
        1. When users ask to delete/update/complete a task, use the task name they mention directly in the tool call
        2. You can match tasks by partial title (case-insensitive) - user says "shopping", you use "going to shopping" as task_identifier
        3. For delete_task/update_task/complete_task, put the task name the user mentioned in the task_identifier parameter
        4. Don't ask users for task IDs - they don't know IDs, they only know task names
        5. Be decisive - if user says "delete the shopping task", immediately call delete_task with task_identifier="shopping"
        6. Provide friendly, conversational responses
        7. Never expose internal system errors to users

        Your available actions:
        - create_task: Create new tasks (requires title, optional description)
        - list_tasks: Show all existing tasks
        - delete_task: Delete a task by its title (use task_identifier parameter)
        - update_task: Update task title or description (use task_identifier parameter)
        - complete_task: Mark a task as completed (use task_identifier parameter)

        EXAMPLES:
        - User: "delete the shopping task" → Call delete_task with task_identifier="shopping"
        - User: "mark the blog post as done" → Call complete_task with task_identifier="blog post"
        - User: "show my tasks" → Call list_tasks
        """

        self.tools = []

    def add_tool(self, tool_spec: Dict[str, Any]):
        """
        Add an MCP tool to the agent's tool registry.

        Args:
            tool_spec: Tool specification dictionary
        """
        self.tools.append(tool_spec)

    def process_request(self, user_input: str, user_id: str, db_session: Session, conversation_history: list = None, conversation_id: str = None) -> str:
        """
        Process a natural language request from a user using OpenRouter API with tool calling.

        Args:
            user_input: Natural language input from user
            user_id: ID of the authenticated user
            db_session: Database session for data access

        Returns:
            Natural language response to the user
        """
        try:
            logger.info(f"Processing request for user {user_id} using OpenRouter API")

            # Build message history
            messages = [{"role": "system", "content": self.system_prompt}]

            # Add conversation history if provided
            if conversation_history:
                messages.extend(conversation_history)

            # Add current user message
            messages.append({"role": "user", "content": user_input})

            # Define tools for task management
            tools = [
                {
                    "type": "function",
                    "function": {
                        "name": "create_task",
                        "description": "Create a new task with a title and optional description",
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
                                }
                            },
                            "required": ["title"]
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "list_tasks",
                        "description": "List all tasks for the user",
                        "parameters": {
                            "type": "object",
                            "properties": {},
                            "required": []
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "delete_task",
                        "description": "Delete a task by its title or ID",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "task_identifier": {
                                    "type": "string",
                                    "description": "The title or ID of the task to delete"
                                }
                            },
                            "required": ["task_identifier"]
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "update_task",
                        "description": "Update a task's title or description",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "task_identifier": {
                                    "type": "string",
                                    "description": "The title or ID of the task to update"
                                },
                                "new_title": {
                                    "type": "string",
                                    "description": "New title for the task"
                                },
                                "new_description": {
                                    "type": "string",
                                    "description": "New description for the task"
                                }
                            },
                            "required": ["task_identifier"]
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "complete_task",
                        "description": "Mark a task as completed",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "task_identifier": {
                                    "type": "string",
                                    "description": "The title or ID of the task to complete"
                                }
                            },
                            "required": ["task_identifier"]
                        }
                    }
                }
            ]

            # Call OpenRouter API with tool support
            # Using GPT-3.5 Turbo - very cheap and supports tools
            response = self.client.chat.completions.create(
                model="openai/gpt-3.5-turbo",  # Cheap model with tool support (~$0.50/M tokens)
                messages=messages,
                tools=tools,
                tool_choice="auto",
                temperature=0.7,
                max_tokens=400  # Reduced to stay within credit limits
            )

            # Check if the model wants to call a tool
            message = response.choices[0].message

            if message.tool_calls and len(message.tool_calls) > 0:
                # Execute the tool call
                tool_call = message.tool_calls[0]
                function_name = tool_call.function.name
                import json

                # Parse function arguments safely
                try:
                    if tool_call.function.arguments:
                        function_args = json.loads(tool_call.function.arguments)
                    else:
                        function_args = {}
                except json.JSONDecodeError as e:
                    logger.error(f"JSON decode error for tool call arguments: {e}")
                    function_args = {}

                logger.info(f"Executing tool: {function_name} with args: {function_args}")

                # Log tool invocation to database
                from ..services.tool_invocation_service import create_tool_invocation, update_tool_invocation_result

                tool_invocation = create_tool_invocation(
                    db_session=db_session,
                    user_id=user_id,
                    conversation_id=conversation_id,
                    tool_name=function_name,
                    tool_arguments=function_args
                )

                try:
                    result = None

                    if function_name == "create_task":
                        # Import task service
                        from ..services.tasks import create_task
                        from ..models.task import TaskCreate

                        # Create the task
                        task_data = TaskCreate(
                            title=function_args.get("title"),
                            description=function_args.get("description", ""),
                            is_completed=False
                        )

                        task = create_task(session=db_session, task=task_data, user_id=user_id)
                        result = {"task_id": task.id, "title": task.title}

                        # Update tool invocation with success
                        update_tool_invocation_result(
                            db_session=db_session,
                            tool_invocation_id=tool_invocation.id,
                            status="success",
                            tool_result=result
                        )

                        return f"I've created the task '{task.title}' for you!"

                    elif function_name == "list_tasks":
                        # Import task service
                        from ..services.tasks import get_tasks_by_user

                        tasks = get_tasks_by_user(session=db_session, user_id=user_id)
                        result = {"task_count": len(tasks), "tasks": [{"id": t.id, "title": t.title} for t in tasks]}

                        # Update tool invocation with success
                        update_tool_invocation_result(
                            db_session=db_session,
                            tool_invocation_id=tool_invocation.id,
                            status="success",
                            tool_result=result
                        )

                        if tasks:
                            task_list = "\n".join([f"- {task.title} {'✓' if task.is_completed else '○'}" for task in tasks])
                            return f"Here are your tasks:\n{task_list}"
                        else:
                            return "You don't have any tasks yet. Would you like to create one?"

                    elif function_name == "delete_task":
                        # Import task service
                        from ..services.tasks import get_tasks_by_user, delete_task

                        task_identifier = function_args.get("task_identifier")

                        # Find the task by title or ID (with fuzzy matching)
                        tasks = get_tasks_by_user(session=db_session, user_id=user_id)
                        task_to_delete = None

                        for task in tasks:
                            # Exact match or partial match (case-insensitive)
                            if (task.id == task_identifier or
                                task.title.lower() == task_identifier.lower() or
                                task_identifier.lower() in task.title.lower()):
                                task_to_delete = task
                                break

                        if task_to_delete:
                            delete_task(session=db_session, task_id=task_to_delete.id, user_id=user_id)
                            result = {"task_id": task_to_delete.id, "title": task_to_delete.title}

                            # Update tool invocation with success
                            update_tool_invocation_result(
                                db_session=db_session,
                                tool_invocation_id=tool_invocation.id,
                                status="success",
                                tool_result=result
                            )

                            return f"I've deleted the task '{task_to_delete.title}'."
                        else:
                            # Update tool invocation with error
                            update_tool_invocation_result(
                                db_session=db_session,
                                tool_invocation_id=tool_invocation.id,
                                status="error",
                                error_message=f"Task not found: {task_identifier}"
                            )
                            return f"I couldn't find a task matching '{task_identifier}'. Please check the task name and try again."

                    elif function_name == "update_task":
                        # Import task service
                        from ..services.tasks import get_tasks_by_user, update_task
                        from ..models.task import TaskUpdate

                        task_identifier = function_args.get("task_identifier")
                        new_title = function_args.get("new_title")
                        new_description = function_args.get("new_description")

                        # Find the task by title or ID (with fuzzy matching)
                        tasks = get_tasks_by_user(session=db_session, user_id=user_id)
                        task_to_update = None

                        for task in tasks:
                            # Exact match or partial match (case-insensitive)
                            if (task.id == task_identifier or
                                task.title.lower() == task_identifier.lower() or
                                task_identifier.lower() in task.title.lower()):
                                task_to_update = task
                                break

                        if task_to_update:
                            task_update = TaskUpdate(
                                title=new_title if new_title else None,
                                description=new_description if new_description else None
                            )
                            updated_task = update_task(session=db_session, task_id=task_to_update.id, task_update=task_update, user_id=user_id)
                            result = {"task_id": task_to_update.id, "title": updated_task.title}

                            # Update tool invocation with success
                            update_tool_invocation_result(
                                db_session=db_session,
                                tool_invocation_id=tool_invocation.id,
                                status="success",
                                tool_result=result
                            )

                            return f"I've updated the task '{updated_task.title}'."
                        else:
                            # Update tool invocation with error
                            update_tool_invocation_result(
                                db_session=db_session,
                                tool_invocation_id=tool_invocation.id,
                                status="error",
                                error_message=f"Task not found: {task_identifier}"
                            )
                            return f"I couldn't find a task matching '{task_identifier}'. Please check the task name and try again."

                    elif function_name == "complete_task":
                        # Import task service
                        from ..services.tasks import get_tasks_by_user, update_task
                        from ..models.task import TaskUpdate

                        task_identifier = function_args.get("task_identifier")

                        # Find the task by title or ID (with fuzzy matching)
                        tasks = get_tasks_by_user(session=db_session, user_id=user_id)
                        task_to_complete = None

                        for task in tasks:
                            # Exact match or partial match (case-insensitive)
                            if (task.id == task_identifier or
                                task.title.lower() == task_identifier.lower() or
                                task_identifier.lower() in task.title.lower()):
                                task_to_complete = task
                                break

                        if task_to_complete:
                            task_update = TaskUpdate(is_completed=True)
                            updated_task = update_task(session=db_session, task_id=task_to_complete.id, task_update=task_update, user_id=user_id)
                            result = {"task_id": task_to_complete.id, "title": task_to_complete.title}

                            # Update tool invocation with success
                            update_tool_invocation_result(
                                db_session=db_session,
                                tool_invocation_id=tool_invocation.id,
                                status="success",
                                tool_result=result
                            )

                            return f"I've marked the task '{updated_task.title}' as completed!"
                        else:
                            # Update tool invocation with error
                            update_tool_invocation_result(
                                db_session=db_session,
                                tool_invocation_id=tool_invocation.id,
                                status="error",
                                error_message=f"Task not found: {task_identifier}"
                            )
                            return f"I couldn't find a task matching '{task_identifier}'. Please check the task name and try again."

                except Exception as tool_error:
                    # Update tool invocation with error
                    logger.error(f"Error executing tool {function_name}: {tool_error}")
                    update_tool_invocation_result(
                        db_session=db_session,
                        tool_invocation_id=tool_invocation.id,
                        status="error",
                        error_message=str(tool_error)
                    )
                    return f"I encountered an error while {function_name.replace('_', ' ')}. Please try again."

            # If no tool call, return the regular response
            ai_response = message.content
            logger.info(f"Received response from OpenRouter API for user {user_id}")

            return ai_response

        except Exception as e:
            import traceback
            logger.error(f"Error processing request for user {user_id}: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            return f"I'm sorry, I encountered an error processing your request. Please try again."