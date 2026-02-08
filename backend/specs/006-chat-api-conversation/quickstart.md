# Quickstart Guide: Chat API, Conversation State & Full-Stack Integration

## Prerequisites
- Python 3.11+
- FastAPI
- Neon PostgreSQL database
- Better Auth for authentication
- OpenAI Agents SDK
- ChatKit frontend components

## Setup Steps

### 1. Environment Configuration
```bash
# Set up environment variables
export DATABASE_URL="postgresql://username:password@localhost:5432/chatdb"
export JWT_SECRET_KEY="your-secret-key-here"
export BETTER_AUTH_SECRET="your-better-auth-secret"
```

### 2. Database Setup
```bash
# Create required tables
# Conversation table
CREATE TABLE conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id VARCHAR(255) NOT NULL,
    title VARCHAR(255),
    status VARCHAR(50) DEFAULT 'active',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

# Message table
CREATE TABLE messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID REFERENCES conversations(id),
    role VARCHAR(20) NOT NULL,
    content TEXT NOT NULL,
    message_type VARCHAR(50) DEFAULT 'text',
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    metadata JSONB
);
```

### 3. API Endpoint Implementation
```python
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from typing import Optional
import jwt
from sqlmodel import Session, select
from datetime import datetime
from .models import Conversation, Message
from .database import get_session
from .ai_agent import process_message_with_agent

app = FastAPI()
security = HTTPBearer()

@app.post("/api/{user_id}/chat")
async def chat_endpoint(
    user_id: str,
    message_request: dict,
    conversation_id: Optional[str] = None,
    token: str = Depends(security),
    db_session: Session = Depends(get_session)
):
    # Validate JWT token
    try:
        payload = jwt.decode(token.credentials, JWT_SECRET_KEY, algorithms=["HS256"])
        authenticated_user_id = payload.get("user_id")

        if authenticated_user_id != user_id:
            raise HTTPException(status_code=401, detail="Unauthorized")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    # Get or create conversation
    if conversation_id:
        conversation = db_session.get(Conversation, conversation_id)
        if not conversation or conversation.user_id != user_id:
            raise HTTPException(status_code=404, detail="Conversation not found")
    else:
        conversation = Conversation(user_id=user_id)
        db_session.add(conversation)
        db_session.commit()
        db_session.refresh(conversation)

    # Save user message
    user_message = Message(
        conversation_id=conversation.id,
        role="user",
        content=message_request["message"]["content"],
        message_type="text"
    )
    db_session.add(user_message)
    db_session.commit()

    # Fetch conversation history for context
    conversation_history = db_session.exec(
        select(Message)
        .where(Message.conversation_id == conversation.id)
        .order_by(Message.timestamp)
    ).all()

    # Process with AI agent
    ai_response = await process_message_with_agent(conversation_history)

    # Save AI response
    ai_message = Message(
        conversation_id=conversation.id,
        role="assistant",
        content=ai_response["content"],
        message_type=ai_response.get("type", "text")
    )
    db_session.add(ai_message)
    db_session.commit()

    return {
        "success": True,
        "message": {
            "id": str(ai_message.id),
            "content": ai_message.content,
            "role": ai_message.role,
            "timestamp": ai_message.timestamp.isoformat(),
            "type": ai_message.message_type
        },
        "conversation_id": str(conversation.id),
        "tool_calls": ai_response.get("tool_calls", [])
    }
```

### 4. Frontend Integration
```javascript
// Example frontend integration with ChatKit
import { useState, useEffect } from 'react';

const ChatInterface = ({ userId, authToken }) => {
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState('');

  const sendMessage = async () => {
    if (!inputText.trim()) return;

    // Add user message to UI immediately
    const userMessage = {
      id: Date.now().toString(),
      content: inputText,
      role: 'user',
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputText('');

    try {
      const response = await fetch(`/api/${userId}/chat`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${authToken}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          message: { content: inputText }
        })
      });

      const data = await response.json();

      if (response.ok) {
        setMessages(prev => [...prev, data.message]);
      } else {
        console.error('Error sending message:', data.error);
      }
    } catch (error) {
      console.error('Network error:', error);
    }
  };

  return (
    <div className="chat-container">
      <div className="messages-list">
        {messages.map(msg => (
          <div key={msg.id} className={`message ${msg.role}`}>
            {msg.content}
          </div>
        ))}
      </div>
      <div className="input-area">
        <input
          type="text"
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
        />
        <button onClick={sendMessage}>Send</button>
      </div>
    </div>
  );
};
```

## Testing the Integration
```bash
# Test the endpoint
curl -X POST \
  http://localhost:8000/api/user123/chat \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message": {
      "content": "Hello, how can you help me?"
    }
  }'
```

## Next Steps
1. Implement the AI agent integration
2. Add MCP tool invocation handling
3. Complete frontend ChatKit integration
4. Add comprehensive error handling
5. Set up monitoring and logging