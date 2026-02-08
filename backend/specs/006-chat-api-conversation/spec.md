# Chat API, Conversation State & Full-Stack Integration Specification

## Overview
This specification defines the full-stack integration of the **chat system**, detailing how user messages flow from ChatKit frontend through the backend and AI agent to produce responses, while maintaining stateless execution and conversation persistence.

## User Scenarios & Testing

### Primary User Scenario
1. User opens the chat interface and authenticates via Better Auth
2. User types a message and submits it to the `/api/{user_id}/chat` endpoint
3. Backend validates JWT token and fetches conversation history from Neon PostgreSQL
4. AI agent processes the user's message with conversation context
5. Backend stores user message and AI response in the database
6. Response is returned to the frontend and displayed to the user
7. All conversation history remains accessible for future interactions

### Test Scenarios
- **Authentication Flow**: Verify JWT validation works correctly and unauthorized requests return 401
- **Message Persistence**: Confirm that both user messages and AI responses are stored with timestamps
- **Conversation Context**: Test that AI agent receives complete conversation history for context-aware responses
- **Stateless Operation**: Verify that identical requests produce consistent results without server-side session state
- **Frontend Integration**: Validate ChatKit components display messages correctly with proper styling

## Functional Requirements

### R1: Chat Endpoint Implementation
- **REQ**: The system SHALL provide a POST endpoint at `/api/{user_id}/chat`
- **REQ**: The endpoint SHALL accept user messages in JSON format with message content and metadata
- **REQ**: The endpoint SHALL return AI-generated responses in JSON format
- **REQ**: The endpoint SHALL validate JWT authentication tokens and return 401 for invalid/missing tokens

### R2: Conversation State Management
- **REQ**: The system SHALL fetch complete conversation history from Neon PostgreSQL for each request
- **REQ**: The system SHALL NOT maintain any server-side session state between requests
- **REQ**: All context for AI processing SHALL come from the database, not memory or cache
- **REQ**: Repeated identical requests SHALL produce consistent results based on database state

### R3: Data Persistence
- **REQ**: The system SHALL store each conversation in a `Conversation` table with user association
- **REQ**: The system SHALL store each message in a `Message` table with conversation reference, timestamp, and sender type
- **REQ**: All timestamps SHALL be stored in UTC with timezone information
- **REQ**: Both user messages AND AI responses SHALL be persisted in the database

### R4: Frontend Integration
- **REQ**: The frontend SHALL use ChatKit components for message display and input
- **REQ**: The frontend SHALL apply Tailwind CSS styling without inline styles
- **REQ**: The frontend SHALL handle authentication flow via Better Auth
- **REQ**: The frontend SHALL communicate with backend via well-defined JSON schema

### R5: AI Agent Integration
- **REQ**: The AI agent SHALL receive conversation history as context for generating responses
- **REQ**: The AI agent SHALL process user messages and generate appropriate responses
- **REQ**: The AI agent SHALL maintain conversational coherence across message exchanges
- **REQ**: The AI agent response time SHALL be under 10 seconds for typical interactions

## Success Criteria

### Quantitative Measures
- 100% of authenticated requests return valid responses within 10 seconds
- 100% of user messages and AI responses are persisted in the database
- 99% uptime for the chat endpoint during business hours
- 95% of conversation context retrieval requests complete within 2 seconds
- 0% server-side session storage used for conversation state

### Qualitative Measures
- Users can seamlessly continue conversations with context awareness
- Authentication protects user data privacy and access
- Message history displays correctly with clear distinction between user and AI messages
- System handles concurrent users without state interference
- Frontend provides smooth, responsive chat experience

## Key Entities

### Conversation Entity
- Unique identifier (UUID)
- User reference (foreign key to user table)
- Created timestamp
- Updated timestamp
- Status (active, archived)

### Message Entity
- Unique identifier (UUID)
- Conversation reference (foreign key to conversation table)
- Sender type (user, ai)
- Content (text)
- Timestamp
- Metadata (message type, status)

### API Contract
- Request: `POST /api/{user_id}/chat` with JSON body containing message content
- Response: JSON object with AI response, conversation ID, and message status
- Authentication: Bearer token in Authorization header
- Error responses: Standard HTTP status codes with JSON error details

## Constraints & Limitations

### Technical Constraints
- Backend MUST NOT store session state; all context comes from database
- MCP tool logic is NOT included; only chat integration and conversation flow
- Conversation history fetch is limited to relevant user data only
- Database queries MUST be optimized to prevent N+1 problems

### Security Constraints
- JWT tokens MUST be validated on each request
- Users can only access their own conversation data
- Message content MUST be sanitized to prevent XSS attacks
- Rate limiting SHOULD be implemented to prevent abuse

## Assumptions

- Better Auth provides JWT tokens for user authentication
- Neon PostgreSQL is available and properly configured
- AI agent is available via existing infrastructure or API
- ChatKit components are properly integrated with the frontend
- Users have stable internet connection for real-time messaging
- Message length is reasonably bounded (under 10,000 characters)