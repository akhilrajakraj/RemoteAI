from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "RemoteAI"
    environment: str = "development"
    host: str = "127.0.0.1"
    port: int = 8000

    database_url: str = "sqlite:///./data/remoteai.db"

    model_provider: str = "ollama"
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "gemma:2b"

    # Optional remote inference endpoint, e.g. a secured Colab tunnel.
    remote_model_url: str | None = None
    remote_model_api_key: str | None = None

    data_dir: Path = Path("data")
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
