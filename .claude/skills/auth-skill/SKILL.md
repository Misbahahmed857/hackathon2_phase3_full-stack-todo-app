# Auth Skill

## Purpose
Handle authentication: signup, signin, password hashing, JWT tokens, Better Auth integration.

## Capabilities
- **Better Auth Setup**: Configure JWT token issuance on Next.js frontend
- **Password Security**: Hash passwords with bcrypt (10+ rounds)
- **JWT Generation**: Create signed tokens with user claims (sub, email, exp)
- **JWT Verification**: Validate tokens in FastAPI middleware
- **Session Management**: Handle token refresh and logout

## Implementation Guide
**Frontend (Better Auth)**:
- Configure Better Auth to issue JWT on login
- Store tokens in httpOnly cookies
- Include `Authorization: Bearer <token>` in API calls

**Backend (FastAPI)**:
- Extract token from Authorization header
- Verify signature using shared secret
- Decode user ID and filter data accordingly

## Security Standards
- Access tokens: 15-60 min expiration
- Refresh tokens: 7-30 days expiration
- Use HS256 or RS256 algorithm
- Store secrets in environment variables