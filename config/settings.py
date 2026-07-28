from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Jarvis"
    MODEL: str = "qwen3:8b"
    OLLAMA_URL: str = "http://localhost:11434"

    class Config:
        env_file = ".env"

settings = Settings()
