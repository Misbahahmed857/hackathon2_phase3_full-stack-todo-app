from sqlmodel import create_engine
import os
from urllib.parse import quote_plus

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

# Create the engine
engine = create_engine(database_url, echo=True)