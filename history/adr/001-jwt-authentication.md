# ADR 001: JWT-Based Authentication

**Date**: 2026-01-23
**Status**: Accepted
**Authors**: Claude Code
**Reviewers**:

## Context

We need to implement secure user authentication for the full-stack web application. The system must support user signup, signin, and protect API endpoints while maintaining a stateless backend architecture as required by the project constitution.

Two primary approaches are available:
1. JWT-based authentication (stateless)
2. Server-side sessions (stateful)

## Decision

We will implement JWT-based authentication for the following reasons:

### Requirements
- Stateless backend (per constitution)
- User isolation and identity verification
- Secure token transmission
- Proper authorization enforcement

### Chosen Solution: JWT-Based Authentication

- Frontend: Better Auth handles user signup/signin and issues JWT tokens
- Backend: FastAPI verifies JWT tokens using shared secret (BETTER_AUTH_SECRET)
- Transport: JWT passed via Authorization: Bearer header
- Identity Source: JWT claims (user_id, email) are authoritative

## Alternatives Considered

### Server-Side Sessions
- **Pros**: Simpler client-side management, server-controlled expiration
- **Cons**: Violates stateless backend constraint, requires session storage, more complex scaling

### OAuth Integration
- **Pros**: Third-party provider support, reduced password management
- **Cons**: More complex setup, not required by spec, vendor lock-in concerns

## Consequences

### Positive
- Complies with stateless backend requirement
- Enables horizontal scaling without session affinity
- Clear separation of authentication and authorization
- Standard HTTP authorization patterns

### Negative
- JWT tokens are larger than session IDs
- No centralized way to revoke active tokens (until expiration)
- Client-side storage considerations (potential XSS concerns)

## Implementation Details

- Token expiration: Short-lived tokens (15 minutes recommended)
- Secret management: Environment variable (BETTER_AUTH_SECRET)
- Error handling: 401 responses for invalid/missing tokens
- Claims: user_id and email extracted from JWT payload

## Validation Criteria

- Users can register and receive valid JWT tokens
- Protected endpoints reject requests without valid tokens (401)
- JWT claims correctly provide user identity
- System maintains stateless behavior