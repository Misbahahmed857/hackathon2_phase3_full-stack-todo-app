# Data Model: Full-Stack Web Integration

## Frontend State Models

### UserSession
- **Properties**:
  - `userId`: string - Unique identifier for the authenticated user
  - `token`: string - JWT token for API authentication
  - `expiresAt`: Date - Token expiration time
  - `isLoggedIn`: boolean - Authentication status

- **State Transitions**:
  - Unauthenticated → Authenticating → Authenticated/LockedOut
  - Authenticated → LoggingOut → Unauthenticated

### TaskUI
- **Properties**:
  - `id`: string - Unique task identifier
  - `title`: string (1-200 chars) - Task title
  - `description`: string (max 1000 chars) - Task description
  - `isCompleted`: boolean - Completion status
  - `createdAt`: Date - Creation timestamp
  - `updatedAt`: Date - Last update timestamp

- **State Transitions**:
  - Pending → Creating → Created/Error
  - Created → Updating → Updated/Error
  - Created → Deleting → Deleted/Error

## Frontend API Models

### APIRequest
- **Properties**:
  - `url`: string - Target endpoint
  - `method`: string - HTTP method (GET, POST, PUT, PATCH, DELETE)
  - `headers`: object - Request headers including Authorization
  - `body`: object - Request payload

### APIResponse
- **Properties**:
  - `success`: boolean - Request success status
  - `data`: object - Response data
  - `error`: object - Error details if request failed
  - `statusCode`: number - HTTP status code

## Validation Rules

### Task Validation (Frontend)
- **Title**: 1-200 characters
- **Description**: 0-1000 characters
- **isCompleted**: boolean type
- **Required fields**: id, title

### API Validation
- **Authorization header**: Must contain valid JWT token
- **Content-Type**: application/json for POST/PUT/PATCH requests
- **Response handling**: Proper error states for 4xx/5xx responses