<!-- SYNC IMPACT REPORT
Version change: N/A -> 1.0.0
Modified principles: N/A (new constitution)
Added sections: All sections from Hackathon III Constitution
Removed sections: Template placeholder sections
Templates requiring updates: N/A
Follow-up TODOs: None
-->

# Hackathon III Constitution
## Spec-Driven Agentic AI Chatbot Development

---

## 1. Purpose

This constitution defines the **mandatory rules, constraints, and principles** for Hackathon III, whose objective is to transform the existing Todo full-stack application into an **AI-powered conversational chatbot** using **MCP (Model Context Protocol)** and **OpenAI Agents SDK**, implemented strictly via **Spec-Driven Development**.

This constitution ensures architectural correctness, security, statelessness, and evaluability under the Agentic Dev Stack methodology.

---

## 2. Mandatory Development Methodology

### 2.1 Spec-Driven Workflow (Non-Negotiable)

All work MUST follow this exact order:

1. Write specification (`/sp.specify`)
2. Generate plan (`/sp.plan`)
3. Generate atomic tasks (`/sp.tasks`)
4. Implement strictly via Claude Code

❌ No phase may be skipped
❌ No direct implementation without an approved spec and plan

---

### 2.2 No Manual Coding Rule

- **Human developers may NOT write application code**
- All source code must be generated or modified exclusively via **Claude Code**
- Humans may only:
  - Write specs
  - Review plans
  - Approve tasks
  - Validate outputs

Violation of this rule invalidates the hackathon submission.

---

## 3. Approved Technology Stack

Only the following technologies are permitted:

| Layer | Technology |
|-----|-----------|
Frontend | OpenAI ChatKit
Backend | Python FastAPI
AI Framework | OpenAI Agents SDK
MCP Server | Official MCP SDK
ORM | SQLModel
Database | Neon Serverless PostgreSQL
Authentication | Better Auth (JWT-based)

❌ No alternative frameworks or libraries are allowed without explicit spec amendment.

---

## 4. Architectural Principles

### 4.1 Stateless Server Architecture

- FastAPI server must be fully stateless
- MCP tools must be stateless
- AI agent must not rely on in-memory state
- All state (tasks, conversations, messages) MUST persist in the database

Server restarts must not affect ongoing conversations.

---

### 4.2 Model Context Protocol (MCP) Compliance

- All task operations MUST be exposed as MCP tools
- AI agents may NOT directly access the database
- AI agents may ONLY interact with the system via MCP tools
- MCP tools must:
  - Validate inputs
  - Enforce user ownership
  - Persist changes via SQLModel

---

### 4.3 Agent-Orchestrated Behavior

- The AI agent is responsible for:
  - Interpreting natural language
  - Selecting appropriate MCP tools
  - Sequencing multiple tool calls when required
- Business logic must NOT be embedded in the chat endpoint

---

## 5. Authentication & Security Rules

### 5.1 Authentication Mechanism

- Authentication is managed via **Better Auth**
- JWT tokens must be issued on the frontend
- JWT must be validated on every backend request
- All chat and MCP operations require authentication

---

### 5.2 User Isolation (Strict)

- Every task, conversation, and message is scoped to `user_id`
- AI agents must act **only on the authenticated user's data**
- Cross-user access is strictly forbidden

Violations constitute a critical security failure.

---

## 6. Feature Scope (Basic Level Only)

Hackathon III is limited to **Basic Level functionality**:

- Conversational task creation
- Conversational task listing
- Conversational task completion
- Conversational task updating
- Conversational task deletion
- Conversation history persistence
- Stateless request handling

❌ No advanced analytics
❌ No voice input
❌ No multi-agent collaboration
❌ No external integrations

---

## 7. Specification Decomposition (Mandatory)

Hackathon III MUST be implemented using **three separate specifications**:

### Spec 4 — AI Agent & Behavior
- Natural language understanding
- Intent detection
- Tool selection rules
- Confirmation and error responses

### Spec 5 — MCP Server & Task Tools
- MCP server setup
- Tool definitions and schemas
- Stateless tool execution
- Database persistence via SQLModel

### Spec 6 — Chat API & Full-Stack Integration
- Chat endpoint (`POST /api/{user_id}/chat`)
- Conversation lifecycle
- Message persistence
- ChatKit frontend integration
- Auth propagation

Combining these concerns into a single spec is not allowed.

---

## 8. Quality & Evaluation Criteria

A submission is considered valid only if:

- All behavior traces directly to a written spec
- MCP tools are used for all task operations
- The chatbot survives server restarts
- Conversations resume correctly
- Errors are handled gracefully
- Codebase shows clear spec → plan → task lineage

---

## 9. Deliverables

The final submission must include:

- `/frontend` — ChatKit UI
- `/backend` — FastAPI + Agents SDK + MCP
- `/specs` — All Hackathon III specifications
- Database migration scripts
- README with setup and usage instructions

---

## 10. Governing Rule

If there is a conflict between:
- Code and specs → **specs win**
- Plans and constitution → **constitution wins**
- Convenience and architecture → **architecture wins**

This constitution is authoritative for Hackathon III.

---

**Version**: 1.0.0 | **Ratified**: 2026-02-06 | **Last Amended**: 2026-02-06