# Quickstart Guide: Authentication & User Identity

**Feature**: 001-auth-identity
**Date**: 2026-01-23

## Overview

This guide explains how to implement JWT-based authentication using Better Auth on the frontend and FastAPI on the backend.

## Prerequisites

- Node.js 18+ (for frontend)
- Python 3.11+ (for backend)
- Neon PostgreSQL database
- BETTER_AUTH_SECRET environment variable

## Environment Setup

### Backend Environment Variables
```bash
BETTER_AUTH_SECRET=your-secret-key-here
DATABASE_URL=postgresql://username:password@neon-host.region.neon.tech/dbname
```

### Frontend Environment Variables
```bash
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:8000
NEXT_PUBLIC_BETTER_AUTH_SECRET=your-secret-key-here
```

## Implementation Steps

### 1. Backend JWT Verification Setup

Create the authentication dependency:

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from jwt.exceptions import InvalidTokenError
from typing import Optional

security = HTTPBearer()

def verify_jwt_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """
    Verify JWT token and return payload
    """
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            settings.better_auth_secret,
            algorithms=["HS256"]
        )
        return payload
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
```

### 2. Protected Route Example

```python
from fastapi import APIRouter, Depends

router = APIRouter()

@router.get("/protected")
async def protected_endpoint(current_user: dict = Depends(verify_jwt_token)):
    return {"user_id": current_user["user_id"], "email": current_user["email"]}
```

### 3. Frontend Better Auth Configuration

Configure Better Auth in your Next.js application:

```typescript
import { BetterAuth } from "better-auth";

export const auth = BetterAuth({
  emailAndPassword: {
    enabled: true,
  },
  jwt: {
    secret: process.env.BETTER_AUTH_SECRET!,
  },
});
```

### 4. Making Authenticated API Calls

On the frontend, attach the JWT token to requests:

```typescript
const makeAuthenticatedRequest = async (url: string, options = {}) => {
  const token = await auth.getSession(); // Get current session token

  return fetch(url, {
    ...options,
    headers: {
      ...options.headers,
      "Authorization": `Bearer ${token}`,
    },
  });
};
```

## Testing the Implementation

### 1. User Registration
- Send POST request to `/api/auth/register` with email and password
- Verify user is created and receives JWT token

### 2. User Login
- Send POST request to `/api/auth/login` with email and password
- Verify valid JWT token is returned

### 3. Protected Resource Access
- Make request to protected endpoint with valid JWT token
- Verify access is granted
- Make request without token to same endpoint
- Verify 401 Unauthorized response

## Common Issues and Solutions

### JWT Secret Mismatch
- Ensure the same `BETTER_AUTH_SECRET` is used on both frontend and backend
- Check environment variables are properly loaded

### Token Expiration
- Handle token expiration gracefully on the frontend
- Implement token refresh mechanisms if needed

### CORS Issues
- Configure proper CORS settings in FastAPI to allow frontend domain