# AI Agent Usage Guide

This document explains how to use the conversational AI agent for task management.

## Overview

The AI agent provides a natural language interface for managing tasks. Users can interact with the system using everyday language to create, list, update, complete, and delete tasks.

## Supported Commands

### Creating Tasks
- "Add a task to buy groceries"
- "Create a task to call the doctor"
- "Remember to water the plants tomorrow"
- "Make a note to finish the report"

### Listing Tasks
- "Show me my tasks"
- "What do I have to do?"
- "List my pending tasks"
- "Show completed tasks"
- "View all my tasks"

### Completing Tasks
- "Mark the homework task as done"
- "Complete the shopping task"
- "Finish the laundry"
- "Check off the meeting task"

### Updating Tasks
- "Change the title of the meeting task"
- "Update the deadline for the report"
- "Edit the description of the project task"

### Deleting Tasks
- "Delete the old task"
- "Remove the cancelled appointment"
- "Cancel the obsolete task"

## Error Handling

The AI agent handles various error conditions gracefully:

- **Ambiguous Requests**: When a request is unclear, the agent will ask for clarification
- **Invalid Commands**: Unknown commands will result in helpful guidance
- **System Errors**: Internal errors are handled without exposing technical details

## Technical Details

- The AI agent operates in a stateless manner
- All data is persisted to the Neon PostgreSQL database
- MCP tools are used for all database operations
- User isolation is enforced at the application level

## Integration

The AI agent is accessible through the chat API endpoint at `/chat/message`.