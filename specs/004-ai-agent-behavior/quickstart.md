# Quickstart Guide: AI Agent & Behavioral Logic

## Overview
This guide provides a quick introduction to implementing and using the conversational AI agent for task management.

## Prerequisites
- Python 3.11+
- OpenAI API key
- MCP SDK installation
- Access to the task management system via MCP tools

## Setup

### 1. Environment Configuration
```bash
# Set up your OpenAI API key
export OPENAI_API_KEY="your-api-key-here"

# Install required dependencies
pip install openai python-dotenv
```

### 2. Initialize the AI Agent
```python
from agents.ai_agent import AIAgent

# Create an instance of the AI agent
agent = AIAgent()
```

### 3. Register MCP Tools
```python
from mcp_tools.task_tools import register_task_tools

# Register the MCP tools with the agent
register_task_tools(agent)
```

## Usage

### Processing a User Request
```python
# Example: User wants to create a task
user_input = "Add a task to buy groceries tomorrow"
response = agent.process_request(user_input, user_id="user123")
print(response)  # Output: "I've added the task 'buy groceries' for tomorrow."
```

### Supported Operations
The AI agent supports the following natural language operations:

1. **Task Creation**: "Add a task to...", "Create a task for...", "Remember to..."
2. **Task Listing**: "Show my tasks", "What do I have to do?", "List pending tasks"
3. **Task Completion**: "Mark as done", "Complete the homework task", "Finish..."
4. **Task Updates**: "Change the deadline", "Update the title", "Modify..."
5. **Task Deletion**: "Delete the meeting task", "Remove...", "Cancel..."

## MCP Tools Interface

The agent communicates with the system exclusively through MCP tools:

- `add_task(title: str, description: str = None, due_date: str = None) -> dict`
- `list_tasks(status: str = "all", limit: int = None) -> list`
- `complete_task(task_id: int) -> bool`
- `update_task(task_id: int, title: str = None, description: str = None, due_date: str = None) -> bool`
- `delete_task(task_id: int) -> bool`

## Error Handling
The agent handles errors gracefully:
- Invalid requests receive helpful clarifications
- System errors return user-friendly messages
- Ambiguous requests ask for clarification

## Example Conversations

### Creating a Task
```
User: "Add a task to call mom this weekend"
Agent: "I've added the task 'call mom' for this weekend."
```

### Listing Tasks
```
User: "What do I have to do today?"
Agent: "You have 2 tasks scheduled for today:
1. Buy groceries (pending)
2. Call mom (pending)"
```

### Completing a Task
```
User: "Mark buy groceries as done"
Agent: "I've marked 'buy groceries' as completed. Great job!"
```

## Testing
Run the following to verify your implementation:
```bash
pytest tests/unit/test_ai_agent.py
pytest tests/integration/test_chat_endpoint.py
```