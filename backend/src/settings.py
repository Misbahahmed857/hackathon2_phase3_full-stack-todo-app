from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    better_auth_secret: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 15
    database_url: str

    class Config:
        env_file = ".env"


settings = Settings()