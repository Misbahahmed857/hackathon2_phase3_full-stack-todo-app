# API Skill

## Purpose
Create RESTful APIs with FastAPI, including middleware and validation.

## Capabilities
- **Endpoint Creation**: CRUD operations with proper HTTP methods
- **Middleware**: JWT authentication, CORS, error handling
- **Validation**: Pydantic models for request/response
- **Documentation**: Auto-generated OpenAPI/Swagger docs
- **Error Handling**: Standardized error responses

## Endpoint Patterns
- `POST /api/auth/signup` - User registration
- `POST /api/auth/signin` - User login
- `GET /api/resources` - List user's resources (requires auth)
- `POST /api/resources` - Create resource (requires auth)
- `PUT /api/resources/{id}` - Update resource (requires auth)
- `DELETE /api/resources/{id}` - Delete resource (requires auth)

## Security Implementation
- Verify JWT on protected routes
- Filter queries by authenticated user ID
- Return 401 for invalid/expired tokens
- Implement rate limiting