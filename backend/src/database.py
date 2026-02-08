from sqlmodel import create_engine, Session, SQLModel
import os
from urllib.parse import quote_plus
from dotenv import load_dotenv
from contextlib import contextmanager

# Import models to ensure they're registered with SQLModel for table creation
from src.models.user import User
from src.models.task import Task
from src.models.conversation import Conversation
from src.models.message import Message
from src.models.tool_invocation import ToolInvocation

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

# Create the engine with connection pooling settings for Neon serverless
# Add SSL parameters for Neon compatibility
engine = create_engine(
    database_url,
    echo=True,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,  # Verify connections before use
    pool_recycle=300,  # Recycle connections every 5 minutes
    connect_args={
        "sslmode": "require",
        "connect_timeout": 30,
    }
)


def create_db_and_tables():
    """Create database tables if they don't exist."""
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session