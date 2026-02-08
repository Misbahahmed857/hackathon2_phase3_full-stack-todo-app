# Data Model: AI Agent & Behavioral Logic

## Overview
This document defines the key data entities for the conversational AI agent that manages user todos through natural language using the OpenAI Agents SDK, while interacting only through MCP tools.

## Key Entities

### Natural Language Intent
**Description**: Represents the user's intention extracted from natural language
**Attributes**:
- intent_type: Enum (CREATE, READ, UPDATE, DELETE, LIST)
- confidence_score: Float (0.0-1.0)
- extracted_parameters: Dictionary (key-value pairs of parameters extracted from the input)

### Task Operation
**Description**: Represents the specific action to be performed on tasks
**Attributes**:
- operation_type: Enum (ADD, LIST, COMPLETE, UPDATE, DELETE)
- task_details: Dictionary (contains task title, description, due_date, etc.)
- target_task_id: Integer (optional, for operations targeting specific tasks)

### Confirmation Response
**Description**: Represents the friendly, conversational response provided after successful operations
**Attributes**:
- response_type: Enum (SUCCESS, ERROR, CONFIRMATION, CLARIFICATION)
- message: String (the actual response text)
- suggested_followup: String (optional follow-up suggestions)

### Conversation Context
**Description**: Contains the current state of the conversation for the AI agent
**Attributes**:
- user_id: String (identifies the authenticated user)
- conversation_history: List of Message objects (chat history)
- current_request: String (the current user input)
- extracted_entities: Dictionary (entities extracted from the current request)

### Message
**Description**: Represents a single message in the conversation
**Attributes**:
- role: Enum (USER, ASSISTANT, SYSTEM)
- content: String (the message content)
- timestamp: DateTime (when the message was created)
- metadata: Dictionary (additional metadata associated with the message)

## Relationships
- A Conversation Context contains multiple Messages
- A Natural Language Intent leads to a Task Operation
- A Task Operation results in a Confirmation Response