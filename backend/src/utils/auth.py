"""
JWT authentication utilities for the chat system.
"""
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer
from pydantic import BaseModel

# Secret key for JWT - in production, this should come from environment variables
SECRET_KEY = "your-secret-key-change-this-in-production"  # Should be set in environment
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

security = HTTPBearer()

class TokenData(BaseModel):
    """Data contained in a JWT token."""
    user_id: str
    username: Optional[str] = None


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create a new JWT access token.

    Args:
        data: Data to encode in the token
        expires_delta: Expiration time for the token

    Returns:
        str: Encoded JWT token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> Optional[TokenData]:
    """
    Verify a JWT token and return the decoded data.

    Args:
        token: JWT token to verify

    Returns:
        TokenData: Decoded token data if valid, None if invalid
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("user_id")
        username: str = payload.get("username")

        if user_id is None:
            return None

        token_data = TokenData(user_id=user_id, username=username)
        return token_data
    except JWTError:
        return None


def get_current_user_from_token(token: str = Depends(security)) -> Optional[TokenData]:
    """
    Get the current user from the JWT token in the request.

    Args:
        token: JWT token from Authorization header

    Returns:
        TokenData: User data if token is valid, raises HTTPException if not
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_data = verify_token(token.credentials)
    if token_data is None:
        raise credentials_exception

    return token_data