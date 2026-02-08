# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is Hackathon III - an AI-powered conversational chatbot for task management built using Spec-Driven Development (SDD). The application transforms a traditional Todo app into a conversational interface using Model Context Protocol (MCP) and OpenAI Agents SDK.

**Architecture**: Stateless FastAPI backend + Next.js frontend with Better Auth authentication.

## Tech Stack

- **Backend**: Python 3.11, FastAPI, SQLModel ORM
- **Frontend**: Next.js 14.2.0, React 18, TailwindCSS, Better Auth
- **AI/Agent**: OpenAI Agents SDK, OpenRouter API
- **MCP**: Model Context Protocol SDK for tool definitions
- **Database**: Neon Serverless PostgreSQL (SQLite for development)
- **Testing**: pytest, pytest-asyncio

## Development Commands

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Create .env file with required variables:
# DATABASE_URL=sqlite:///./test.db
# BETTER_AUTH_SECRET=your-secret-key
# OPENROUTER_API_KEY=your-openrouter-key

# Run backend server
uvicorn src.main:app --reload --port 8000
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev  # Runs on http://localhost:3000
```

### Testing
```bash
cd backend

# Run all tests
pytest

# Run specific test file
pytest tests/unit/test_ai_agent.py

# Run with verbose output
pytest -v

# Run integration tests
pytest tests/integration/

# Run e2e tests
pytest tests/e2e/
```

## Code Architecture

### Backend Structure

**Core Layers**:
1. **API Layer** (`backend/src/api/v1/`): FastAPI routers for auth, tasks, chat endpoints
2. **Agent Layer** (`backend/src/agents/`): AI agent logic using OpenAI SDK
   - `ai_agent.py`: Main conversational agent that processes natural language
   - `intent_classifier.py`: Classifies user intent (CREATE_TASK, LIST_TASKS, etc.)
3. **MCP Server** (`backend/src/mcp_server/`): Stateless tools for task operations
   - `tools/`: Individual tool implementations (add_task, list_tasks, complete_task, etc.)
   - `server.py`: MCP server FastAPI app exposing tool endpoints
4. **Services** (`backend/src/services/`): Business logic for auth, tasks, chat, conversations
5. **Models** (`backend/src/models/`): SQLModel database models (User, Task, Conversation, Message)

**Key Architectural Constraints**:
- **Stateless Design**: All state persists in database; no in-memory state
- **MCP Tool Pattern**: AI agent ONLY interacts with data via MCP tools, never direct database access
- **User Isolation**: All operations scoped to authenticated user_id
- **Tool Registry**: `backend/src/mcp_tools/tool_registry.py` manages tool definitions and execution

### Frontend Structure

**Next.js App Router** (`frontend/src/app/`):
- `/login` and `/register`: Authentication pages using Better Auth
- `/dashboard`: Traditional task management UI
- `/chat`: Conversational AI chatbot interface using ChatKit component

**Components** (`frontend/src/components/`):
- `ChatKit.jsx`: Main chat interface for conversational task management
- `ProtectedRoute.jsx`: HOC for auth-protected routes
- `TaskForm.jsx`, `TaskItem.jsx`: Traditional task UI components

### Database Models

All models inherit from SQLModel and include automatic timestamps:
- **User**: id, username, email, hashed_password
- **Task**: id, title, description, completed, user_id, created_at, updated_at, due_date
- **Conversation**: id, user_id, title, created_at, updated_at
- **Message**: id, conversation_id, role (user/assistant), content, created_at

### Authentication Flow

1. Better Auth handles JWT token generation on frontend
2. Backend validates JWT via `backend/src/api/deps.py:get_current_user()`
3. `user_id` extracted from token and used for all database queries
4. Protected routes require valid JWT in Authorization header

## Spec-Driven Development Workflow

This project uses Spec-Driven Development (SDD) methodology. All features MUST follow this workflow:

### Mandatory Workflow Order
1. **Specification** (`/sp.specify`): Write feature requirements
2. **Plan** (`/sp.plan`): Generate architectural design
3. **Tasks** (`/sp.tasks`): Create atomic, testable tasks
4. **Implementation**: Execute via Claude Code (humans may NOT write application code)

### Project Structure for SDD
- `.specify/memory/constitution.md`: Project principles and rules (see below)
- `specs/<feature>/spec.md`: Feature requirements
- `specs/<feature>/plan.md`: Architecture decisions
- `specs/<feature>/tasks.md`: Testable implementation tasks
- `history/prompts/`: Prompt History Records (PHRs)
- `history/adr/`: Architecture Decision Records (ADRs)

### Key SDD Principles from Constitution

**Stateless Architecture** (CRITICAL):
- FastAPI and MCP tools must be fully stateless
- All state persists in Neon PostgreSQL via SQLModel
- Server restarts must not affect conversations

**MCP Compliance**:
- AI agents may ONLY interact via MCP tools
- No direct database access from agents
- Tools must validate inputs and enforce user ownership

**User Isolation**:
- Every operation scoped to authenticated `user_id`
- Cross-user access is a critical security failure

**Feature Scope** (Basic Level Only):
- Conversational task CRUD operations
- Conversation history persistence
- NO advanced analytics, voice, or external integrations

### Prompt History Records (PHRs)

After implementation work, create PHRs to document user interactions:
- Location: `history/prompts/constitution/`, `history/prompts/<feature-name>/`, or `history/prompts/general/`
- Template: `.specify/templates/phr-template.prompt.md`
- Stages: constitution | spec | plan | tasks | red | green | refactor | explainer | misc | general

### Architecture Decision Records (ADRs)

For architecturally significant decisions, suggest (but don't auto-create):
```
📋 Architectural decision detected: <brief>
   Document reasoning and tradeoffs? Run `/sp.adr <decision-title>`
```

Test for ADR significance:
- **Impact**: Long-term consequences (framework, data model, API, security)?
- **Alternatives**: Multiple viable options considered?
- **Scope**: Cross-cutting, influences system design?

If ALL true, suggest ADR creation and wait for user consent.

## Environment Variables

### Backend (.env)
```
DATABASE_URL=sqlite:///./test.db  # Or PostgreSQL connection string
BETTER_AUTH_SECRET=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
OPENROUTER_API_KEY=your-openrouter-api-key
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
ALLOWED_ORIGINS=http://localhost:3000,*
```

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=same-secret-as-backend
```

## Development Guidelines

### When Working on Features
1. **Read the Constitution**: Check `.specify/memory/constitution.md` for mandatory constraints
2. **Check Existing Specs**: Review `specs/<feature>/` to understand implemented features
3. **Follow SDD Workflow**: Never implement without spec → plan → tasks
4. **Use MCP Tools**: For AI agent work, always use tool registry pattern
5. **Test Thoroughly**: Add unit tests (`tests/unit/`), integration tests (`tests/integration/`), and e2e tests (`tests/e2e/`)

### Code References
When discussing code, use format `file_path:line_number` for precise references:
```
The agent processes requests in backend/src/agents/ai_agent.py:73
```

### Working with MCP Tools
1. Tool definitions: `backend/src/mcp_server/tools/tool_schemas.py`
2. Tool implementations: `backend/src/mcp_server/tools/<tool_name>_tool.py`
3. Register tools: `backend/src/mcp_tools/tool_registry.py`
4. Agent invokes tools via registry, NOT direct database access

### Testing Strategy
- **Unit tests**: Individual MCP tools and agent functions
- **Integration tests**: API endpoints, database interactions, tool execution
- **E2E tests**: Full conversation flows with chat endpoint

## Common Pitfalls to Avoid

1. **Breaking Statelessness**: Never store conversation state in memory or module-level variables
2. **Direct DB Access from Agent**: Always use MCP tools for data operations
3. **Skipping SDD Workflow**: Do not implement features without spec/plan/tasks
4. **Cross-User Data Leaks**: Always filter queries by authenticated user_id
5. **Hardcoded Secrets**: Use .env files, never commit secrets

## Current Active Feature

Branch: `004-ai-agent-behavior`
- Python 3.11 + OpenAI Agents SDK
- Model Context Protocol (MCP) SDK
- FastAPI integration
- Neon Serverless PostgreSQL (via SQLModel ORM)

See `specs/004-ai-agent-behavior/` for full specification and implementation details.
