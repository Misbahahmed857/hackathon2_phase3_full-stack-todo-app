# API Contract: Authentication Endpoints

**Feature**: 001-auth-identity
**Contract Version**: 1.0
**Date**: 2026-01-23

## Authentication Endpoints

### Register User
- **POST** `/api/auth/register`
- **Description**: Creates a new user account
- **Request Body**:
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```
- **Responses**:
  - 200: User created successfully
  - 400: Invalid input (validation errors)
  - 409: User already exists

### Login User
- **POST** `/api/auth/login`
- **Description**: Authenticates user and returns JWT token
- **Request Body**:
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```
- **Response** (200):
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```
- **Responses**:
  - 200: Successful login
  - 400: Invalid input
  - 401: Invalid credentials

### Verify Token
- **GET** `/api/auth/verify`
- **Description**: Verifies JWT token validity
- **Headers**:
  - Authorization: `Bearer <jwt_token>`
- **Response** (200):
```json
{
  "valid": true,
  "user_id": "uuid-string",
  "email": "user@example.com"
}
```
- **Responses**:
  - 200: Valid token
  - 401: Invalid or expired token

## Protected Resource Access

### Example Protected Endpoint
- **GET** `/api/tasks`
- **Description**: Retrieves user's tasks
- **Headers**:
  - Authorization: `Bearer <jwt_token>`
- **Response** (200):
```json
{
  "tasks": [...]
}
```
- **Responses**:
  - 200: Successful retrieval
  - 401: Missing or invalid token

## Error Responses

All error responses follow this structure:
```json
{
  "detail": "Error message describing the issue"
}
```

## JWT Token Structure

### Header
```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

### Payload
```json
{
  "user_id": "uuid-string",
  "email": "user@example.com",
  "exp": 1234567890,
  "iat": 1234567890
}
```