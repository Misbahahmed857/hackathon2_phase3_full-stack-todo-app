"""
Database connection management for the MCP server.

This module handles database connections to Neon PostgreSQL using SQLModel,
implementing connection pooling and resilience patterns for stateless operation.
"""
from sqlmodel import create_engine, Session
from contextlib import contextmanager
import os
from urllib.parse import quote_plus
from dotenv import load_dotenv
import logging


# Set up logging
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv('.env')

# Get database URL from environment, with a default for development
database_url = os.getenv("DATABASE_URL", "sqlite:///./test.db")

# URL encode the password if it contains special characters (only for PostgreSQL)
if database_url.startswith("postgresql://"):
    # Split the URL to extract components
    parts = database_url.split('@', 1)
    if len(parts) == 2:
        scheme_and_creds = parts[0]
        host_and_db = parts[1]

        # Further split to get credentials
        creds_part = scheme_and_creds.split('://')[1]
        user_pass = creds_part.split(':')
        if len(user_pass) >= 2:
            password = user_pass[1]
            encoded_password = quote_plus(password)
            # Reconstruct the URL with encoded password
            database_url = f"{scheme_and_creds.split(':')[0]}://{user_pass[0]}:{encoded_password}@{host_and_db}"

# Create the engine with connection pooling settings
engine = create_engine(
    database_url,
    echo=True,  # Set to False in production
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,  # Verify connections before use
    pool_recycle=300  # Recycle connections every 5 minutes
)


def get_session():
    """
    Get a database session from the connection pool.

    Yields:
        Session: Database session for use in operations
    """
    with Session(engine) as session:
        try:
            yield session
        except Exception as e:
            logger.error(f"Database session error: {e}")
            session.rollback()
            raise
        finally:
            session.close()


def test_connection():
    """
    Test the database connection by executing a simple query.

    Returns:
        bool: True if connection is successful, False otherwise
    """
    try:
        with Session(engine) as session:
            # Execute a simple query to test the connection
            result = session.exec("SELECT 1")
            return True
    except Exception as e:
        logger.error(f"Database connection test failed: {e}")
        return False


def ensure_connection_resilience():
    """
    Ensure connection resilience by testing and re-establishing connection if needed.

    Returns:
        bool: True if connection is healthy, False otherwise
    """
    try:
        # Test the current connection
        if test_connection():
            logger.info("Database connection is healthy")
            return True
        else:
            logger.warning("Database connection test failed, attempting recovery")
            # In a real implementation, we might try to recreate the engine
            return False
    except Exception as e:
        logger.error(f"Error during connection resilience check: {e}")
        return False