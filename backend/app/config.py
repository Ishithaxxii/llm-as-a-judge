from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    database_url: str = "sqlite+aiosqlite:///./judgeai.db"
    groq_api_key: str | None = None
    gemini_api_key: str | None = None
    default_judges: list[str] = ["groq:llama-3.3-70b-versatile", "gemini:gemini-2.5-flash"]
    max_judges_per_request: int = 4
    judge_timeout_seconds: int = 30
    cors_origins: list[str] = ["http://localhost:5173"]
    mock_judges: bool = False

@lru_cache
def get_settings() -> Settings:
    return Settings()