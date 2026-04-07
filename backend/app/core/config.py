from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    groq_api_key: str

    # Database
    database_url: str

    # # Ollama
    # ollama_base_url: str = "http://localhost:11434"
    # embedding_model: str = "nomic-embed-text"

    # LLM
    llm_model: str = "llama-3.3-70b-versatile"

    embedding_model: str = "all-MiniLM-L6-v2"

    # App
    app_name: str = "BLR Rentals API"
    debug: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()