# Validation Skill

## Purpose
Validate inputs, tokens, and data integrity across the application.

## Capabilities
- **Email Validation**: RFC 5322 format, max 320 chars
- **Password Validation**: Min 8 chars, complexity requirements
- **JWT Validation**: Verify signature, expiration, claims
- **Request Validation**: Type checking, required fields, sanitization
- **Security Checks**: SQL injection, XSS prevention

## Validation Rules
**Passwords**: 8+ chars, uppercase, lowercase, digit, special char
**Emails**: Valid format, unique in database
**JWT**: Valid signature, not expired, contains required claims
**Inputs**: Trim whitespace, escape special characters

## Implementation
- Use Pydantic models in FastAPI
- Use Zod schemas in Next.js
- Validate before processing any authentication request