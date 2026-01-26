# API Contracts: Full-Stack Web Integration

## Authentication Endpoints

### POST /api/v1/auth/login
**Description**: Authenticate user and return JWT token
**Request**:
- Headers: `Content-Type: application/json`
- Body: `{ "email": string, "password": string }`
- Expected Response: `200 OK` with `{ "access_token": string, "token_type": "bearer" }`
- Error Responses: `401 Unauthorized`, `422 Validation Error`

### POST /api/v1/auth/register
**Description**: Register new user
**Request**:
- Headers: `Content-Type: application/json`
- Body: `{ "email": string, "password": string }`
- Expected Response: `200 OK` with `{ "message": string }`
- Error Responses: `400 Bad Request`, `422 Validation Error`

## Task Management Endpoints

### GET /api/v1/tasks
**Description**: Retrieve authenticated user's tasks
**Request**:
- Headers: `Authorization: Bearer <token>`
- Expected Response: `200 OK` with `Task[]`
- Error Responses: `401 Unauthorized`, `403 Forbidden`

### POST /api/v1/tasks
**Description**: Create new task for authenticated user
**Request**:
- Headers: `Authorization: Bearer <token>`, `Content-Type: application/json`
- Body: `{ "title": string(1-200), "description": string(max 1000), "is_completed": boolean }`
- Expected Response: `201 Created` with `Task`
- Error Responses: `401 Unauthorized`, `422 Validation Error`

### GET /api/v1/tasks/{task_id}
**Description**: Retrieve specific task for authenticated user
**Request**:
- Headers: `Authorization: Bearer <token>`
- Expected Response: `200 OK` with `Task`
- Error Responses: `401 Unauthorized`, `404 Not Found`

### PUT /api/v1/tasks/{task_id}
**Description**: Update entire task for authenticated user
**Request**:
- Headers: `Authorization: Bearer <token>`, `Content-Type: application/json`
- Body: `{ "title": string(1-200), "description": string(max 1000), "is_completed": boolean }`
- Expected Response: `200 OK` with `Task`
- Error Responses: `401 Unauthorized`, `404 Not Found`, `422 Validation Error`

### PATCH /api/v1/tasks/{task_id}
**Description**: Partially update task for authenticated user
**Request**:
- Headers: `Authorization: Bearer <token>`, `Content-Type: application/json`
- Body: `{ "title"?: string(1-200), "description"?: string(max 1000), "is_completed"?: boolean }`
- Expected Response: `200 OK` with `Task`
- Error Responses: `401 Unauthorized`, `404 Not Found`, `422 Validation Error`

### DELETE /api/v1/tasks/{task_id}
**Description**: Delete task for authenticated user
**Request**:
- Headers: `Authorization: Bearer <token>`
- Expected Response: `204 No Content`
- Error Responses: `401 Unauthorized`, `404 Not Found`

## Task Response Schema

```json
{
  "id": "string",
  "title": "string",
  "description": "string",
  "is_completed": "boolean",
  "user_id": "string",
  "created_at": "string",
  "updated_at": "string"
}
```

## Error Response Schema

```json
{
  "detail": "string"
}
```