# Tasks: Task Management (CRUD + Ownership)

**Feature**: Task Management (CRUD + Ownership)
**Created**: 2026-01-26
**Status**: Draft
**Input**: `/specs/002-task-management/spec.md`

## Phase 1: Setup

- [X] T001 Create directory structure for task management feature in backend/src/models, backend/src/services, backend/src/api/v1
- [X] T002 Update main.py to include task management routes

## Phase 2: Foundation

- [X] T003 [P] Create Task model with user_id foreign key, validation rules in backend/src/models/task.py
- [X] T004 [P] Create task service with CRUD operations in backend/src/services/tasks.py
- [X] T005 [P] Create task API endpoints with authentication enforcement in backend/src/api/v1/tasks.py

## Phase 3: [US1] Create Personal Tasks

**Goal**: Enable authenticated users to create personal tasks with titles and descriptions
**Independent Test**: User can register/login, create a task with title and description, and verify it's stored with correct ownership

- [X] T006 [US1] Implement task creation endpoint POST /api/v1/tasks
- [X] T007 [US1] Add validation for task title (1-200 chars) and description (0-1000 chars)
- [X] T008 [US1] Associate created tasks with authenticated user ID
- [X] T009 [US1] Return created task with all details in response

## Phase 4: [US2] View Own Tasks

**Goal**: Allow users to view only their own tasks, preventing access to others' tasks
**Independent Test**: Create multiple users with tasks, verify each user only sees their own tasks

- [X] T010 [US2] Implement task listing endpoint GET /api/v1/tasks
- [X] T011 [US2] Filter tasks by authenticated user ID in queries
- [X] T012 [US2] Prevent access to other users' tasks
- [X] T013 [US2] Return only user's tasks in response

## Phase 5: [US3] Update Own Tasks

**Goal**: Enable users to update their tasks including toggling completion status
**Independent Test**: User can update their task's title, description, or completion status

- [X] T014 [US3] Implement task update endpoint PUT /api/v1/tasks/{task_id}
- [X] T015 [US3] Implement task patch endpoint PATCH /api/v1/tasks/{task_id}
- [X] T016 [US3] Verify user owns the task before updating
- [X] T017 [US3] Update task completion status correctly

## Phase 6: [US4] Delete Own Tasks

**Goal**: Allow users to delete their own tasks
**Independent Test**: User can delete their own task but cannot delete others' tasks

- [X] T018 [US4] Implement task deletion endpoint DELETE /api/v1/tasks/{task_id}
- [X] T019 [US4] Verify user owns the task before deletion
- [X] T020 [US4] Remove task from database on successful deletion

## Phase 7: Testing & Validation

- [X] T021 Add unit tests for task service functions
- [X] T022 Add integration tests for task API endpoints
- [X] T023 Test ownership enforcement (users can't access other users' tasks)
- [X] T024 Test validation rules (title length, description length)
- [X] T025 Test all CRUD operations work as expected

## Phase 8: Polish & Documentation

- [X] T026 Update OpenAPI documentation for new endpoints
- [X] T027 Add error handling and validation error responses
- [X] T028 Add logging for task operations
- [X] T029 Review and optimize database queries for performance

## Dependencies

- Task T003 (Task model) blocks T004 (Task service)
- Task T004 (Task service) blocks T005 (Task API endpoints)
- Task T005 (Task API endpoints) blocks all user story tasks

## Parallel Execution Opportunities

- T001, T002 can run in parallel with other setup tasks
- T003, T004, T005 can run in parallel (different files, sequential dependencies)
- US1-US4 can be developed in parallel after foundation is complete

## Implementation Strategy

**MVP Scope**: Complete Phase 1, 2, and Phase 3 ([US1]) to deliver basic task creation functionality.

**Incremental Delivery**:
1. MVP: Task creation (Phase 1, 2, 3)
2. Add retrieval (Phase 4)
3. Add updates (Phase 5)
4. Add deletion (Phase 6)
5. Add testing and polish (Phases 7, 8)