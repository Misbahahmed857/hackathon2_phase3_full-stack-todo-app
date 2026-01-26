from pydantic import BaseModel
from typing import Optional


class UserRegistration(BaseModel):
    email: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class JWTPayload(BaseModel):
    user_id: str
    email: str
    exp: int
    iat: int