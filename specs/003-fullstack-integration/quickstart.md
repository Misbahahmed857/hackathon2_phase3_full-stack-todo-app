# Quickstart: Full-Stack Web Integration

## Prerequisites

- Node.js 18+ for frontend
- Python 3.11+ for backend
- Neon PostgreSQL database
- Better Auth configured

## Frontend Setup

### 1. Install Dependencies
```bash
cd frontend
npm install next@16 react react-dom @types/react @types/node @types/react-dom
npm install better-auth
npm install tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

### 2. Configure API Client
Create `frontend/src/lib/api.js` with centralized API client that attaches JWT tokens automatically.

### 3. Setup Authentication Provider
Create `frontend/src/components/AuthProvider/` with Better Auth integration.

## Backend Setup

### 1. Verify Backend is Running
Ensure the backend server with task endpoints is operational:
- `/api/v1/tasks` (GET, POST)
- `/api/v1/tasks/{task_id}` (GET, PUT, PATCH, DELETE)

### 2. Verify Database Connection
Ensure Neon PostgreSQL connection is established and task tables exist.

## Frontend Development

### 1. Create Task Components
- `TaskList` component to display user's tasks
- `TaskForm` component for creating/updating tasks
- `TaskItem` component for individual task display

### 2. Implement Protected Routes
Create middleware or higher-order components to protect routes requiring authentication.

### 3. Connect UI to API
- Fetch tasks after successful authentication
- Handle JWT token attachment to API requests
- Implement CRUD operations in the UI

## Testing Integration

### 1. Authentication Flow
- Navigate to login page
- Enter valid credentials
- Verify redirect to dashboard
- Confirm tasks load from backend

### 2. Task Operations
- Create new task via UI → verify appears in list
- Update task → verify changes persist
- Toggle completion → verify state updates
- Delete task → verify removal from list

### 3. Persistence Validation
- Refresh page after operations
- Verify data persists in database
- Confirm JWT token handling works correctly