# Data Model: Authentication & User Identity

**Feature**: 001-auth-identity
**Date**: 2026-01-23
**Model Version**: 1.0

## User Entity

### User Model (SQLModel)

```python
class User(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: str = Field(unique=True, nullable=False, max_length=255)
    hashed_password: str = Field(nullable=False)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships if needed
    # tasks: List["Task"] = Relationship(back_populates="user")
```

### User Registration Input

```python
class UserRegistration(BaseModel):
    email: str
    password: str
```

### User Login Input

```python
class UserLogin(BaseModel):
    email: str
    password: str
```

### JWT Token Payload

```python
class JWTPayload(BaseModel):
    user_id: str
    email: str
    exp: int
    iat: int
```

### JWT Token Response

```python
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
```

## Database Schema

### Users Table
- `id`: UUID (Primary Key, Default: uuid_generate_v4())
- `email`: VARCHAR(255) (Unique, Not Null)
- `hashed_password`: TEXT (Not Null)
- `is_active`: BOOLEAN (Default: True)
- `created_at`: TIMESTAMP (Default: NOW())
- `updated_at`: TIMESTAMP (Default: NOW())

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
  "user_id": "<user-uuid>",
  "email": "user@example.com",
  "exp": <expiration_timestamp>,
  "iat": <issued_at_timestamp>
}
```

## Security Considerations

- Passwords must be hashed using bcrypt or similar
- JWT secret must be stored securely in environment variables
- Token expiration should be reasonable (e.g., 15 minutes for access tokens)
- User IDs in JWT should be UUIDs for security