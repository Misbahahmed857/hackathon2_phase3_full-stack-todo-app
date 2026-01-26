# Research: Authentication & User Identity

**Feature**: 001-auth-identity
**Date**: 2026-01-23
**Research Phase**: Phase 0

## Better Auth Capabilities

Better Auth is a modern authentication library for React/Next.js applications that provides:
- Email/password authentication
- Social login (though not used in this feature per spec)
- JWT token issuance on successful authentication
- Session management (though we'll focus on JWT-only approach)
- TypeScript support

Key configuration options:
- JWT token structure and claims
- Token expiration times
- Custom user fields to include in tokens

## FastAPI JWT Verification Patterns

FastAPI provides several approaches for JWT token verification:
- Using python-jose library for JWT decoding and verification
- Dependency injection for authentication
- Custom security schemes
- Exception handling for invalid tokens

Common patterns:
- Create a dependency function that verifies JWT and returns user info
- Apply this dependency to protected endpoints
- Return 401 responses for invalid/missing tokens

## JWT Claims Structure

Standard JWT claims for authentication:
- `sub`: Subject (user ID)
- `exp`: Expiration time
- `iat`: Issued at time
- Custom claims:
  - `user_id`: Unique identifier for the user
  - `email`: User's email address

## Authorization Header Format

HTTP Authorization header format:
- `Authorization: Bearer <jwt_token>`
- FastAPI dependency can extract and validate this header

## Environment Variables

For secure JWT verification:
- `BETTER_AUTH_SECRET`: Shared secret between frontend and backend
- Should be stored in environment variables on both sides