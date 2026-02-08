# Data Model: Chat API, Conversation State & Full-Stack Integration

## Entity: Conversation
- **id**: string (UUID) - Primary key, unique identifier for conversation
- **user_id**: string - Foreign key to user table, identifies conversation owner
- **created_at**: datetime - Timestamp when conversation was created
- **updated_at**: datetime - Timestamp when conversation was last updated
- **title**: string (optional) - User-friendly name for the conversation
- **status**: string - Current status (active, archived)

### Relationships
- One-to-many with Message entity (one conversation to many messages)

### Validation Rules
- user_id must reference an existing user
- created_at must be in the past
- updated_at must be >= created_at

## Entity: Message
- **id**: string (UUID) - Primary key, unique identifier for message
- **conversation_id**: string - Foreign key to conversation table
- **role**: string - Message role (user, assistant, system)
- **content**: string - Text content of the message
- **timestamp**: datetime - When the message was created
- **message_type**: string - Type of message (text, tool_call, tool_response)
- **metadata**: json (optional) - Additional message metadata

### Relationships
- Many-to-one with Conversation entity (many messages to one conversation)

### Validation Rules
- conversation_id must reference an existing conversation
- role must be one of (user, assistant, system)
- content must not exceed 10,000 characters
- timestamp must be in the past

## API Contract Schema

### Request Schema: `/api/{user_id}/chat`
```json
{
  "message": {
    "content": "string (required)",
    "role": "string (optional, default: user)"
  },
  "conversation_id": "string (optional, creates new if not provided)"
}
```

### Response Schema: `/api/{user_id}/chat`
```json
{
  "success": "boolean",
  "message": {
    "id": "string",
    "content": "string",
    "role": "string",
    "timestamp": "datetime",
    "type": "string"
  },
  "conversation_id": "string",
  "tool_calls": [
    {
      "name": "string",
      "arguments": "object"
    }
  ]
}
```

### Error Response Schema
```json
{
  "error": "string",
  "code": "string",
  "details": "object (optional)"
}
```