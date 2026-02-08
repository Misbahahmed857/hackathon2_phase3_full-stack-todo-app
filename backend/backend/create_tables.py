#!/usr/bin/env python3
"""Script to create database tables for the application."""

from sqlmodel import SQLModel, create_engine
from src.models.user import User
from src.models.task import Task
import os

# Get database URL from environment
database_url = os.getenv("DATABASE_URL", "sqlite:///./test.db")

# Create the engine
engine = create_engine(database_url, echo=True)

def create_db_and_tables():
    """Create all tables in the database."""
    print("Creating database tables...")
    SQLModel.metadata.create_all(engine)
    print("Tables created successfully!")

if __name__ == "__main__":
    create_db_and_tables()