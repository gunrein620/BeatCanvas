"""
Configuration settings for BeatCanvas backend.
Loads environment variables from .env file.
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    OPENAI_API_KEY: str
    SOUNDFONT_PATH: str = "../soundfonts/GeneralUserGS.sf2"
    TEMP_DIR: str = "./temp"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Global settings instance
settings = Settings()
