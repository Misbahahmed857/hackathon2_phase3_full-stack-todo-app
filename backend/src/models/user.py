from sqlmodel import SQLModel, Field
from uuid import uuid4
from datetime import datetime
from typing import Optional
import sqlalchemy.sql.functions
from sqlalchemy import Column, DateTime


class UserBase(SQLModel):
    email: str = Field(unique=True, nullable=False, max_length=255)


class User(UserBase, table=True):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    hashed_password: str = Field(nullable=False)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(sa_column=Column(DateTime(timezone=True), default=sqlalchemy.sql.functions.now()))
    updated_at: datetime = Field(sa_column=Column(DateTime(timezone=True), default=sqlalchemy.sql.functions.now(), onupdate=sqlalchemy.sql.functions.now()))


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: str
    is_active: bool
    created_at: datetime
    updated_at: datetime


class UserUpdate(SQLModel):
    email: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None