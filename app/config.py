from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./monetization.db"
    OLLAMA_URL: str = "http://localhost:11434"

    class Config:
        env_file = ".env"

settings = Settings()