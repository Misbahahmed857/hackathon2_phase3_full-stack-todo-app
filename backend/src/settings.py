from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    better_auth_secret: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 15
    database_url: str
    openrouter_api_key: Optional[str] = None
    openrouter_base_url: Optional[str] = "https://openrouter.ai/api/v1"

    class Config:
        env_file = ".env"


settings = Settings()